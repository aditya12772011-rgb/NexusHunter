import sys
import requests
import whois
import re
import datetime
import socket
import ssl
from urllib.parse import urlparse
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

def print_banner():
    """Displays an aggressive, bright red cyber security banner."""
    banner = f"""
{Fore.LIGHTRED_EX}███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
{Fore.RED}      >> Advanced Security Threat Analyzer <<
{Fore.LIGHTRED_EX}================================================={Style.RESET_ALL}"""
    print(banner)

def get_target_url():
    print(f"\n{Fore.YELLOW}[?] Enter the target URL or Domain (e.g., example.com):{Style.RESET_ALL}")
    user_input = input(f" └─► URL/Domain: ").strip()
    
    parsed = urlparse(user_input)
    if not parsed.scheme:
        target_url = "https://" + user_input
    else:
        target_url = user_input
    return target_url

def extract_emails(whois_data):
    whois_str = str(whois_data)
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', whois_str)
    return list(set(emails))

# 1. CORE SCANNER (Firewall, Server, SSL & WHOIS)
def core_infra_scan(url, domain, protocol):
    print(f"\n{Fore.LIGHTRED_EX}[*] Executing Core Infrastructure Scan...{Style.RESET_ALL}")
    server_banner = "Unknown"
    status_code = "N/A"
    fw_detected = "None"
    
    # Resolve IP
    try:
        ip_address = socket.gethostbyname(domain)
    except:
        ip_address = "Failed to Resolve"

    # SSL Check
    ssl_status = "N/A"
    if protocol == "https":
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    expire_date_str = cert['notAfter']
                    expire_date = datetime.datetime.strptime(expire_date_str, '%b %d %H:%M:%S %Y %Z')
                    days_left = (expire_date - datetime.datetime.now()).days
                    ssl_status = f"Valid ({days_left} days remaining)"
        except:
            ssl_status = "Invalid/Expired Certificate"

    # Firewall & Banner Grabbing
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        server_banner = response.headers.get('Server', 'Not Disclosed')
        status_code = str(response.status_code)
        fw_keywords = ['cloudflare', 'cloudfront', 'sucuri', 'akamai', 'incapsula', 'mod_security']
        for fw in fw_keywords:
            if fw in server_banner.lower() or any(fw in str(val).lower() for val in response.headers.values()):
                fw_detected = fw.upper()
                break
    except:
        print(f" {Fore.RED}[-] HTTP Request Failed.")

    # WHOIS
    registrar, country = "Unknown", "Unknown"
    found_emails = []
    try:
        w_info = whois.whois(domain)
        registrar = w_info.registrar if w_info.registrar else "Unknown"
        country = w_info.country if w_info.country else "Unknown"
        found_emails = extract_emails(w_info)
    except:
        pass

    # Dashboard Output
    print(f"\n{Fore.LIGHTRED_EX}┌──────────────── [ INFRASTRUCTURE DETAILS ] ────────────────┐")
    print(f" {Fore.WHITE}Target Domain : {Fore.YELLOW}{domain}")
    print(f" {Fore.WHITE}IP Address    : {Fore.LIGHTYELLOW_EX}{ip_address}")
    print(f" {Fore.WHITE}Protocol      : {Fore.GREEN if protocol=='https' else Fore.RED}{protocol.upper()}")
    print(f" {Fore.WHITE}HTTP Status   : {Fore.LIGHTGREEN_EX}{status_code}")
    print(f" {Fore.WHITE}SSL Status    : {Fore.LIGHTBLUE_EX}{ssl_status}")
    print(f" {Fore.WHITE}Server Banner : {Fore.LIGHTBLUE_EX}{server_banner}")
    print(f" {Fore.WHITE}Firewall/WAF  : {Fore.GREEN + fw_detected if fw_detected != 'None' else Fore.RED + 'None'}")
    print(f" {Fore.WHITE}Registrar     : {Fore.LIGHTYELLOW_EX}{registrar} ({country})")
    if found_emails:
        print(f" {Fore.WHITE}OSINT Emails  : {Fore.LIGHTCYAN_EX}{', '.join(found_emails[:3])}")
    print(f"{Fore.LIGHTRED_EX}└────────────────────────────────────────────────────────────┘")

# 2. HTTP SECURITY HEADERS AUDIT
def audit_security_headers(url):
    print(f"\n{Fore.LIGHTRED_EX}[*] Auditing HTTP Security Headers...{Style.RESET_ALL}")
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        headers = response.headers
        
        security_headers = {
            "Strict-Transport-Security": "Protects against MITM attacks",
            "X-Frame-Options": "Prevents Clickjacking vulnerabilities",
            "Content-Security-Policy": "Mitigates XSS and data injection attacks",
            "X-Content-Type-Options": "Prevents MIME-sniffing exploits"
        }
        
        print(f"\n{Fore.LIGHTRED_EX}┌────────────────── [ SECURITY HEADERS ] ──────────────────┐")
        for header, desc in security_headers.items():
            if header in headers:
                print(f" {Fore.GREEN}[✔] {header:<30} : PRESENT")
            else:
                print(f" {Fore.RED}[✘] {header:<30} : MISSING ({desc})")
        print(f"{Fore.LIGHTRED_EX}└──────────────────────────────────────────────────────────┘")
    except:
        print(f" {Fore.RED}[-] Header analysis failed. Could not connect.")

# 3. FAST PORT SCANNER
def scan_popular_ports(domain):
    print(f"\n{Fore.LIGHTRED_EX}[*] Scanning Critical Network Ports...{Style.RESET_ALL}")
    ports = [21, 22, 23, 25, 80, 443, 8080]
    port_mapping = {21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 80: "HTTP", 443: "HTTPS", 8080: "HTTP-ALT"}
    
    print(f"\n{Fore.LIGHTRED_EX}┌────────────────────── [ PORT SCAN ] ─────────────────────┐")
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0)
            result = sock.connect_ex((domain, port))
            if result == 0:
                print(f" {Fore.RED}[!] Port {port:<5} ({port_mapping[port]:<8}) : OPEN (Potential Attack Surface)")
            else:
                print(f" {Fore.GREEN}[✔] Port {port:<5} ({port_mapping[port]:<8}) : CLOSED")
            sock.close()
        except:
            pass
    print(f"{Fore.LIGHTRED_EX}└──────────────────────────────────────────────────────────┘")

# 4. ROBOTS.TXT DISCOVERY
def analyze_robots_txt(url):
    print(f"\n{Fore.LIGHTRED_EX}[*] Parsing robots.txt for Hidden Paths...{Style.RESET_ALL}")
    parsed_url = urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    
    try:
        response = requests.get(robots_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        if response.status_code == 200:
            print(f"\n{Fore.LIGHTRED_EX}┌──────────────────── [ ROBOTS.TXT ] ────────────────────┐")
            lines = response.text.split('\n')
            disallowed_paths = [line for line in lines if line.strip().lower().startswith('disallow:')]
            
            if disallowed_paths:
                print(f" {Fore.YELLOW}[!] Disallowed Directories Found (Potential Sensitive Paths):")
                for path in disallowed_paths[:5]: # Show top 5
                    print(f"   ─► {path}")
            else:
                print(f" {Fore.GREEN}[✔] robots.txt exists but contains no hidden paths.")
            print(f"{Fore.LIGHTRED_EX}└────────────────────────────────────────────────────────┘")
        else:
            print(f" {Fore.GREEN}[✔] robots.txt not found (Status {response.status_code}). No paths leaked.")
    except:
        print(f" {Fore.RED}[-] Failed to fetch robots.txt")

# MAIN ENGINE MENU
def main():
    print_banner()
    url = get_target_url()
    parsed_url = urlparse(url)
    domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
    protocol = parsed_url.scheme

    while True:
        print(f"\n{Fore.LIGHTCYAN_EX}┌── [ NEXUS ENGINE CONTROL PANEL ] ────────────────────────┐")
        print("│ 1. Run Core Infrastructure & Firewall Scan               │")
        print("│ 2. Audit HTTP Security Headers                           │")
        print("│ 3. Scan Critical Network Ports                           │")
        print("│ 4. Analyze robots.txt for Directory Leaks                │")
        print("│ 5. Execute All Scans                                     │")
        print("│ 6. Exit Nexus Analyzer                                   │")
        print(f"{Fore.LIGHTCYAN_EX}└──────────────────────────────────────────────────────────┘")
        
        choice = input(f"{Fore.YELLOW} └─► Select Option (1-6): {Style.RESET_ALL}").strip()
        
        if choice == "1":
            core_infra_scan(url, domain, protocol)
        elif choice == "2":
            audit_security_headers(url)
        elif choice == "3":
            scan_popular_ports(domain)
        elif choice == "4":
            analyze_robots_txt(url)
        elif choice == "5":
            core_infra_scan(url, domain, protocol)
            audit_security_headers(url)
            scan_popular_ports(domain)
            analyze_robots_txt(url)
        elif choice == "6":
            print(f"\n{Fore.RED}[+] Exiting Nexus. Stay Secure!{Style.RESET_ALL}\n")
            break
        else:
            print(f"{Fore.RED}[!] Invalid choice! Please select between 1 and 6.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
  
