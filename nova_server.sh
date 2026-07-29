#!/bin/bash
# ════════════════════════════════════════════════════════════════════════
# NOVA NATIVE WEB SERVER & REAL-WORLD TOOL ENGINE (PORT 8080)
# ════════════════════════════════════════════════════════════════════════

PORT=8080
echo -e "\033[38;5;51m[*] Booting Nova Native HTTP Server on port $PORT...\033[0m"
echo -e "\033[38;5;226m[+] Serving directory: $(pwd)\033[0m"
echo -e "\033[38;5;46m[+] Access your generated Web UI at: http://127.0.0.1:$PORT/index.html\033[0m"
echo -e "\033[38;5;196m[!] Press Ctrl+C to stop the Nova server.\033[0m"

# Pure Bash HTTP Server loop to serve files without Python dependency
while true; do
  {
    read -r request
    path=$(echo "$request" | awk '{print $2}')
    if [ "$path" == "/" ] || [ -z "$path" ]; then path="/index.html"; fi
    file=".${path}"
    
    if [ -f "$file" ]; then
      echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r"
      cat "$file"
    else
      echo -e "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r"
      echo "404 - Nova Silicon Node Not Found"
    fi
  } | nc -l -p $PORT -q 1 > /dev/null 2>&1
done
