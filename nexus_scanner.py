import sys
import requests
import socket
import re
from urllib.parse import urlparse
from colorama import Fore, Style, init

# Initialize Colorama for styling
init(autoreset=True)

def print_banner():
    print(f"""
{Fore.LIGHTRED_EX}      _   _                         _   _               _             
{Fore.LIGHTRED_EX}     | \ | | ___  _  _  _  _  ___  | | | | _  _  _ _   | |_  ___  _ _ 
{Fore.LIGHTRED_EX}     |  ` |/ -_)\ \ // _| || |(_-<  | |_| || || ' \   |  _|/ -_)| '_|
{Fore.LIGHTRED_EX}     |_|\_|\___|/_\_\\__|\_,_|/__/   \___/  \_,_||_||_|  \__|\___||_|  
{Fore.RED}     [================================================================]
{Fore.RED}     >> ENGINE MODE: AUTOMATED THREAT INTELLIGENCE & RECON SUMMARIZER
{Fore.RED}     >> DEVELOPED BY: ADITYA | ELITE CYBER SECURITY SYSTEM
{Fore.LIGHTRED_EX}     [================================================================]""")

def extract_emails_from_text(text):
    return list(set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', str(text))))

def main():
    print_banner()
    
    print(f"\n{Fore.YELLOW}[?] ENTER TARGET DOMAIN OR URL (e.g., http://example.com or google.com):{Style.RESET_ALL}")
    user_input = input(f" {Fore.LIGHTRED_EX}└──► {Style.RESET_ALL}").strip()
    
    if not user_input:
        print(f"{Fore.RED}[!] Target cannot be empty. Exiting.")
        sys.exit()

    parsed = urlparse(user_input)
    if parsed.scheme:
        protocol_used = parsed.scheme.upper()
        domain = parsed.netloc if parsed.netloc else parsed.path
        url = user_input
    else:
        domain = parsed.path
        protocol_used = "HTTPS"
        url = f"https://{domain}"

    print(f"\n{Fore.LIGHTCYAN_EX}[*] Nexus Scanner is running... Please wait while profiling infrastructure...{Style.RESET_ALL}")

    try:
        ip_address = socket.gethostbyname(domain)
    except:
        ip_address = "Failed to Resolve IP"

    server_banner = "Not Disclosed"
    firewall = "None Detected"
    missing_headers = []
    ssl_status = "Valid" if protocol_used == "HTTPS" else "No SSL (Plaintext HTTP)"
    osint_emails = []

    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (NexusHunter Engine)'}, timeout=5, allow_redirects=True)
        protocol_used = urlparse(res.url).scheme.upper()
        if protocol_used == "HTTP":
            ssl_status = "No SSL (Plaintext HTTP)"

        server_banner = res.headers.get('Server', 'Hidden/Protected')
        
        fw_keywords = ['cloudflare', 'cloudfront', 'sucuri', 'akamai', 'incapsula', 'mod_security']
        for fw in fw_keywords:
            if fw in server_banner.lower() or any(fw in str(v).lower() for v in res.headers.values()):
                firewall = fw.upper()
                break

        for h in ["Strict-Transport-Security", "X-Frame-Options", "Content-Security-Policy"]:
            if h not in res.headers:
                missing_headers.append(h)
                
    except requests.exceptions.RequestException:
        if not parsed.scheme and url.startswith("https://"):
            try:
                url = f"http://{domain}"
                protocol_used = "HTTP"
                ssl_status = "No SSL (Plaintext HTTP)"
                res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (NexusHunter Engine)'}, timeout=5)
                server_banner = res.headers.get('Server', 'Hidden/Protected')
            except:
                protocol_used = "FAILED"
                ssl_status = "Host Unreachable"
        else:
            protocol_used = "FAILED"
            ssl_status = "Host Unreachable"

    try:
        intel_res = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=6)
        if intel_res.status_code == 200:
            osint_emails = extract_emails_from_text(intel_res.json())
    except:
        pass

    print(f"\n{Fore.LIGHTRED_EX}[+] SECURITY AUDIT COMPLETE! GENERATING THREAT SUMMARY:{Style.RESET_ALL}")
    print(f"{Fore.RED}================================================================={Style.RESET_ALL}")
    
    print(f" {Fore.LIGHTRED_EX}• IP Address      :{Style.RESET_ALL} {Fore.LIGHTYELLOW_EX}{ip_address}")
    print(f" {Fore.LIGHTRED_EX}• Protocol/Scheme :{Style.RESET_ALL} {protocol_used}")
    print(f" {Fore.LIGHTRED_EX}• SSL Status      :{Style.RESET_ALL} {Fore.CYAN}{ssl_status}")
    print(f" {Fore.LIGHTRED_EX}• Server Banner   :{Style.RESET_ALL} {server_banner}")
    print(f" {Fore.LIGHTRED_EX}• Firewall Status :{Style.RESET_ALL} {Fore.GREEN + firewall if firewall != 'None Detected' else Fore.RED + 'None (Exposed Edge)'}")
    
    print(f"\n {Fore.YELLOW}[+] HARVESTED OSINT EMAILS:{Style.RESET_ALL}")
    if osint_emails:
        for email in osint_emails[:5]:
            print(f"  └──► {Fore.CYAN}{email}")
    else:
        print(f"  └──► {Fore.GREEN}No public business emails exposed in standard certificate logs.")

    print(f"\n {Fore.RED}[!] POTENTIAL ATTACK VECTORS & VULNERABILITIES:{Style.RESET_ALL}")
    has_threats = False

    if firewall == "None Detected":
        print(f"  ├── [CRITICAL] DDoS & Layer-7 Flood Risk: No active WAF found.")
        has_threats = True

    if missing_headers:
        print(f"  ├── [HIGH] Clickjacking & Data Injection: Missing defenses: {', '.join(missing_headers)}.")
        has_threats = True

    if protocol_used == "HTTP":
        print(f"  ├── [CRITICAL] Man-In-The-Middle (MITM) Attack: Plaintext HTTP protocol in use.")
        has_threats = True

    if osint_emails:
        print(f"  └── [MEDIUM] Targeted Social Engineering: Exposed email vectors detected.")
        has_threats = True

    if not has_threats:
        print(f"  └── [✔] No immediate high-risk perimeter attack vectors identified.")

    print(f"\n{Fore.LIGHTRED_EX}================================================================={Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()
          
