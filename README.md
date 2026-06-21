# 🛡️ NexusHunter - Advanced Security Threat Analyzer

NexusHunter is an interactive command-line security auditing tool written in Python. It allows developers and security enthusiasts to audit web infrastructure, calculate real-time security scores, detect web application firewalls, and automatically export scan reports.

---

## 🚀 Features

- **🔴 Aggressive Red Dashboard:** Sleek and clean cyber-security theme built for terminal environments.
- **🧱 Advanced Firewall (WAF) Detection:** Identifies proxy layers like Cloudflare, Cloudfront, Akamai, and Sucuri.
- **📈 Security Score Calculator:** Analyzes various vectors and rates the website safety from `0` to `100`.
- **📜 SSL and Protocol Inspector:** Evaluates certificate validity and catches insecure HTTP connections.
- **📂 Automated Report Generation:** Automatically saves all vulnerability and scan summaries into `nexus_report.txt`.

---

## 🛠️ How to Install & Run

Follow these exact steps to clone, set up, and run NexusHunter on your system:

### 1. Clone the official repository:
``git clone https://github.com/aditya12772011-rgb/NexusHunter.git
cd NexusHunter
chmod +x nexus.sh
python3 nexus_scanner.py
📊 Terminal Preview Example
███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
      >> Advanced Security Threat Analyzer <<
=================================================

┌──────────────── [ INFRASTRUCTURE DETAILS ] ────────────────┐
 Target Domain : example.com
 IP Address    : 93.184.216.34
 Protocol      : HTTPS
 HTTP Status   : 200
 SSL Status    : Valid (124 days remaining)
 Server Banner : ECS (ECY/8BB3)
 Firewall/WAF  : None
 SECURITY SCORE: 85/100
└────────────────────────────────────────────────────────────┘

⚠️ Legal Disclaimer
This repository is built strictly for educational and ethical security auditing purposes only. Running web analysis against servers without prior explicit authorization from the owner is illegal. The author holds no liability for any misuse or legal actions.
🤝 Support & Contribution
If you find this project useful, please drop a ⭐️ to show support! Issues and Pull Requests are highly welcomed.




