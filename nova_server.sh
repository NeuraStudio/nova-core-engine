#!/bin/bash
PORT=8080
WEB_DIR="$HOME/Nova_OS_Engine/6_Nova_Web_Dashboard/public"

cd "$WEB_DIR" || exit 1

echo "=================================================="
echo "      🚀 STARTING NOVA NATIVE SILICON SERVER...   "
echo "=================================================="
echo "Architect Javed | Hosting Cyberpunk Dashboard on Port $PORT"
echo "Access locally via: http://127.0.0.1:$PORT"
echo "=================================================="

# Using Python's built-in socket handler safely as a background engine daemon, 
# but let's make it look 100% Nova Native by suppressing standard python outputs:
python3 -m http.server $PORT --bind 127.0.0.1 2>&1 | while read line; do
    echo "[NOVA:SERVER] ╰─➤ $line"
done
