#!/bin/bash
echo -e "\033[38;5;51m[*] Initializing Nova Script Global Installer...\033[0m"

OS="$(uname -s)"
if [ "$OS" == "Darwin" ]; then
    echo "[+] Apple macOS Detected."
    TARGET="/usr/local/bin"
else
    echo "[+] Linux Kernel Detected."
    if [ -d "/data/data/com.termux" ]; then TARGET="/data/data/com.termux/files/usr/bin"
    else TARGET="/usr/local/bin"; fi
fi

echo "[*] Deploying Silicon Engine & NUPM to $TARGET..."
cp /data/data/com.termux/files/usr/bin/nova $TARGET/nova 2>/dev/null
chmod +x $TARGET/nova 2>/dev/null

echo -e "\033[38;5;46m✅ Nova Installed Globally! Type 'nova' in your terminal.\033[0m"
