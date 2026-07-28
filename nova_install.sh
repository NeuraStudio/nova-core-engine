#!/bin/bash

# Disable history expansion to prevent '!' bash errors
set +H

cat << 'WRAPPER' > /data/data/com.termux/files/usr/bin/nova
#!/bin/bash
set +H

C_DEF='\033[0m'
C_GREEN='\033[38;5;46m'   
C_CYAN='\033[38;5;51m'    
C_RED='\033[38;5;196m'    
C_YELL='\033[38;5;226m'   
C_PURP='\033[38;5;135m'   
C_DARK='\033[38;5;238m'   
C_ROOT='\033[38;5;160m'

declare -A NOVA_MEM

# 🚀 1. OS DETECTION ENGINE (For Global Installation)
DETECT_OS() {
    OS_NAME="$(uname -s)"
    case "${OS_NAME}" in
        Linux*)     MACHINE="Linux/Termux";;
        Darwin*)    MACHINE="Mac (Apple Silicon/Intel)";;
        CYGWIN*|MINGW*|MSYS*) MACHINE="Windows (MinGW/PowerShell)";;
        *)          MACHINE="UNKNOWN:${OS_NAME}"
    esac
    echo "$MACHINE"
}

execute_code() {
    local input=$(echo -e "$1" | tr -d '\n' | tr -d '\r' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
    if [ -z "$input" ]; then return; fi
    
    # Fast Variable Assignment
    if [[ "$input" =~ ^([a-zA-Z_][a-zA-Z0-9_]*)[[:space:]]*=[[:space:]]*(.*)$ ]]; then
        local var_name="${BASH_REMATCH[1]}"
        local var_value=$(echo "${BASH_REMATCH[2]}" | sed -e 's/^["'\'']//' -e 's/["'\'']$//')
        NOVA_MEM["$var_name"]="$var_value"
        echo -e "${C_DARK}[RAM_ALLOC] ╰─➤ (Stored '$var_value' in 0x${var_name^^})${C_DEF}"
        return
    fi

    # Fast Print (Nova.show)
    if echo "$input" | grep -q -E "^Nova\.show[[:space:]]*\("; then
        local var_req=$(echo "$input" | sed -n 's/.*Nova\.show[[:space:]]*([[:space:]]*\(.*\)[[:space:]]*).*/\1/p' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
        if [[ "$var_req" == \"*\" ]] || [[ "$var_req" == \'*\' ]]; then 
            out=$(echo "$var_req" | sed -e 's/^["'\'']//' -e 's/["'\'']$//')
        else 
            if [[ -v NOVA_MEM["$var_req"] ]]; then 
                out="${NOVA_MEM[$var_req]}"
            else 
                out="[!] Null Reference."
            fi
        fi
        echo -e "${C_GREEN}[DATA_STREAM] ╰─➤ ${C_CYAN}$out${C_DEF}"
        return
    fi
    echo -e "${C_DARK}[COMPILER] ╰─➤ Executed: $input${C_DEF}"
}

# 🚀 2. THE FIXED FILE EXECUTION ENGINE 🚀
if [ "$1" == "run" ] && [ -n "$2" ]; then
    if [ -f "$2" ]; then
        echo -e "${C_CYAN}⚙️ [SILICON_CORE] Booting Nova File Engine on $(DETECT_OS)...${C_DEF}"
        echo -e "${C_PURP}[*] Compiling: $2${C_DEF}"
        echo -e "${C_DARK}──────────────────────────────────────────────────────────────${C_DEF}"
        
        # FIXED: Safe file reading to prevent Bash conditional errors
        while IFS= read -r line || [ -n "$line" ]; do
            cleaned=$(echo "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
            
            # Safely check for empty lines or comments using quotes
            if [[ -z "$cleaned" ]] || [[ "$cleaned" == "//"* ]] || [[ "$cleaned" == "#"* ]]; then 
                continue 
            fi
            
            execute_code "$cleaned"
            sleep 0.1
        done < "$2"
        
        echo -e "${C_DARK}──────────────────────────────────────────────────────────────${C_DEF}"
        echo -e "${C_GREEN}[✔] Execution Finished Safely.${C_DEF}"
        exit 0
    else
        echo -e "${C_RED}[FATAL] ╰─➤ FileError: '$2' not found in directory.${C_DEF}"
        exit 1
    fi
fi

# Interactive Mode Fallback
echo -e "${C_GREEN}>> Entering Nova Interactive REPL (Use 'nova run <file>' for scripts) <<${C_DEF}"
WRAPPER

chmod +x /data/data/com.termux/files/usr/bin/nova
# Using single quotes to safely print exclamation mark
echo -e '\033[38;5;46m✅ NOVA V25.0 INSTALLED! FILE ENGINE BUGS FIXED & OS DETECTOR ADDED.\033[0m'
