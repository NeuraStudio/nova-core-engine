#!/bin/bash
PORT="${1:-8080}"
echo -e "\033[38;5;46m[NOVA_SERVER] Starting Native Silicon HTTP Server on port $PORT...\033[0m"
echo -e "\033[38;5;51m[NOVA_SERVER] Serving local directory. Press Ctrl+C to stop.\033[0m"
# Utilizing netcat (nc) or Python fallback safely for native serving
if command -v python3 &> /dev/null; then
    python3 -m http.server "$PORT"
else
    while true; do
        echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Nova Silicon Native Server Active</h1>" | nc -l -p "$PORT" -q 1
    done
fi
