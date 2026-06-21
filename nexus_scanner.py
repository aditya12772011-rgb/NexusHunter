import sys
import time
import socket
import json

# Ensure requests is available for the public DNS API and HTTP header parsing
try:
    import requests
except ImportError:
    print("[!] Error: This script requires the 'requests' library.")
    print("    Please install it using: pip install requests")
    sys.argv = [sys.argv[0], "--exit"]  # Force a clean failure state if missing
    requests = None

# Proceed only if critical dependencies are satisfied
if requests is not None:
    # -------------------------------------------------------------------------
    # 3. INTERACTIVE SLOW-PRINTING ANSI BANNER
    # -------------------------------------------------------------------------
    # Native ANSI Escape Codes for styling (Cyan, Green, Yellow, Reset)
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"

    # Sleek cyber-themed ASCII banner body
    BANNER_TEXT = rf"""
{CYAN}=====================================================================
{GREEN}  _   _ ________  ___   _ _____   _   _ _   _ _   _ _____ _____ ______ 

 | \ | |  ___|  \/  | | | /  ___| | | | | | | | \ | |_   _|  ___| ___ \
 |  \| | |__ | .  . | | | \ `--.  | |_| | | | |  \| | | | | |__ | |_/ /
 | . ` |  __|| |\/| | | | |`--. \ |  _  | | | | . ` | | | |  __||    / 
 | |\  | |___| |  | | |_| /\__/ / | | | | |_| | |\  | | | | |___| |\ \ 
 \_| \_/\____/\_|  |_/\___/\____/  \_| |_/\___/\_| \_/ \_/ \____/\_| \_|
                                                                     
                  -- INFRASTRUCTURE MAPPING TOOL --                  
{CYAN}====================================================================={RESET}
"""

    # Render banner with a progressive character-by-character slow-printing typing effect
    for char in BANNER_TEXT:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.002)  # Micro-delay for a fast yet highly visible fluid typewriter stream
    print("\n")

    # Initialize active target session variables
    active_target = ""
    target_ip = ""

    # -------------------------------------------------------------------------
    # INITIAL TARGET ACQUISITION
    # -------------------------------------------------------------------------
    while not active_target:
        user_input = input(f"{YELLOW}[*] Enter initial target domain (e.g., example.com): {RESET}").strip()
        if not user_input:
            print(f"{YELLOW}[!] Target domain cannot be blank.{RESET}\n")
            continue
        
        # Clean protocol prefixes if mistakenly entered by the user
        if user_input.startswith("http://"):
            user_input = user_input[7:]
        elif user_input.startswith("https://"):
            user_input = user_input[8:]
        if "/" in user_input:
            user_input = user_input.split("/")[0]

        print(f" {CYAN}└──►{RESET} Resolving initial infrastructure signature for: {user_input}...")
        try:
            # Resolve domain target to IPv4 address dynamically using native socket library
            target_ip = socket.gethostbyname(user_input)
            active_target = user_input
            print(f" {GREEN}└──► Success!{RESET} Target locked: {active_target} [{target_ip}]\n")
        except socket.gaierror:
            print(f" {YELLOW}[!] Error: Could not resolve domain '{user_input}'. Please check connection/domain syntax.{RESET}\n")

    # -------------------------------------------------------------------------
    # 1. CORE MENU LOOP SYSTEM
    # -------------------------------------------------------------------------
    while True:
        # Display the active target workspace badge
        print(f"{CYAN}[ ACTIVE WORKSPACE: {GREEN}{active_target}{CYAN} ({target_ip}) ]{RESET}")
        print("1. Display Consolidated Infrastructure Summary (Passive parsing)")
        print("2. Audit Core Legitimate Web Service Connections (Socket handshake)")
        print("3. Resolve Upstream Public DNS Topography (dns.google API)")
        print("4. Shift Active Workspace (Dynamic target realignment)")
        print("5. Terminate Operational Instance (Safe exit)")
        
        choice = input(f"\n{YELLOW}NEXUS-HUNTER > Enter choice (1-5): {RESET}").strip()
        print(f"{CYAN}---------------------------------------------------------------------{RESET}")

        # -------------------------------------------------------------------------
        # OPTION 1: DISPLAY CONSOLIDATED INFRASTRUCTURE SUMMARY
        # -------------------------------------------------------------------------
        if choice == "1":
            print(f"[*] Fetching passive infrastructure summary for {active_target}...")
            
            # Setup realistic User-Agent to avoid getting instantly blocked by standard firewalls
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NexusHunter/1.0"}
            
            try:
                # Attempt connection via HTTPS; fall back to HTTP if necessary
                url = f"https://{active_target}"
                try:
                    response = requests.get(url, headers=headers, timeout=5)
                except requests.exceptions.SSLError:
                    url = f"http://{active_target}"
                    response = requests.get(url, headers=headers, timeout=5)

                # Extraction and extraction analytics for structured metrics output
                server_banner = response.headers.get("Server", "Undetected / Hidden")
                hsts_status = "Active / Enforced" if "Strict-Transport-Security" in response.headers else "Missing / Insecure"
                content_type = response.headers.get("Content-Type", "Unknown").split(";")[0]
                powered_by = response.headers.get("X-Powered-By", "None Disclosed")
                
                # Format text data cleanly into targeted bullet-point elements
                print(f"\n• Target Target Mapping Summary:")
                print(f"  └──► Resolve Target:  {active_target}")
                print(f"  └──► Resolved IPv4:   {target_ip}")
                print(f"  └──► Status Code:     {response.status_code}")
                print(f"  └──► Server Banner:   {server_banner}")
                print(f"  └──► HSTS Policy:     {hsts_status}")
                print(f"  └──► Content Engine:  {content_type}")
                print(f"  └──► Tech Stack Tag:  {powered_by}")
                
            except requests.exceptions.RequestException as error_msg:
                print(f" [!] Error: Failed to gather HTTP application metrics safely.")
                print(f"  └──► Diagnostic Failure Reason: {error_msg}")
            print(f"\n{CYAN}---------------------------------------------------------------------{RESET}")

        # -------------------------------------------------------------------------
        # OPTION 2: AUDIT CORE LEGITIMATE WEB SERVICE CONNECTIONS
        # -------------------------------------------------------------------------
        elif choice == "2":
            # Core standard system application gateways to check
            target_ports = [80, 443, 8080]
            print(f"[*] Auditing core service connectivity on standard application gateways...")
            print(f"[*] Testing handshake latency to target IP: {target_ip}\n")
            
            print(f"• Active Infrastructure Connectivity Audit Matrix:")
            for port in target_ports:
                # Instantiating a clean, isolated socket connection channel for each check
                audit_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Ensure the tool remains highly interactive by applying low application timeouts
                audit_socket.settimeout(2.5)
                
                start_time = time.time()
                # Safely execute connection attempt (returns an error indicator instead of throwing an exception)
                conn_result = audit_socket.connect_ex((target_ip, port))
                end_time = time.time()
                
                # Check for standard return value 0 indicating successful handshake execution
                if conn_result == 0:
                    latency = (end_time - start_time) * 1000
                    print(f"  └──► Port {port:<4} [OPEN]   --> Handshake Complete in {latency:.2f}ms")
                else:
                    print(f"  └──► Port {port:<4} [CLOSED] --> Port timed out or rejected connection request")
                
                # Cleanup socket resources efficiently
                audit_socket.close()
            print(f"\n{CYAN}---------------------------------------------------------------------{RESET}")

        # -------------------------------------------------------------------------
        # OPTION 3: RESOLVE UPSTREAM PUBLIC DNS TOPOGRAPHY
        # -------------------------------------------------------------------------
        elif choice == "3":
            print(f"[*] Querying upstream cloud mapping infrastructure (dns.google)...")
            
            # Key record maps to analyze standard resource allocation arrays
            record_types = ["A", "AAAA", "MX", "TXT", "NS"]
            print(f"• Querying Topographical Target Mapping Framework for {active_target}:")
            
            for record in record_types:
                # Query Google's public JSON API resolution interface securely over HTTPS
                api_endpoint = f"https://dns.google{active_target}&type={record}"
                try:
                    dns_response = requests.get(api_endpoint, timeout=5)
                    if dns_response.status_code == 200:
                        dns_data = dns_response.json()
                        
                        # Verify 'Answer' block exists inside the structured JSON reply array
                        if "Answer" in dns_data:
                            print(f"  ├── Record Category: [{record}]")
  
