#!/bin/bash

# Clear the terminal screen for a clean look
clear

# Check if required python libraries are installed
echo "[*] Checking dependencies..."
python3 -c "import requests, whois, colorama" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "[!] Missing libraries. Installing now..."
    pip install requests python-whois colorama
else
    echo "[+] All dependencies are satisfied."
fi

echo "------------------------------------------------"
# Run the Python script
python3 nexus_scanner.py
