#!/bin/bash
TARGET="$1"
echo -e "\033[38;5;226m[REAL_EXEC] Executing live packet reconnaissance on: $TARGET\033[0m"
if command -v nmap &> /dev/null; then
    nmap -p 80,443,22 "$TARGET"
else
    # Fallback to standard ping & port check if nmap isn't pre-installed
    nc -z -v -w2 "$TARGET" 80 443 22 2>&1 || ping -c 2 "$TARGET"
fi
