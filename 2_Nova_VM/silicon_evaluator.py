import sys, re, os, subprocess, time

# ANSI Colors
C_DEF = '\033[0m'
C_GREEN = '\033[38;5;46m'
C_CYAN = '\033[38;5;51m'
C_RED = '\033[38;5;196m'
C_YELL = '\033[38;5;226m'
C_PURP = '\033[38;5;135m'
C_DARK = '\033[38;5;238m'
C_ROOT = '\033[38;5;160m'

# Native Nova Functions
def nova_show(*args):
    print(f"{C_GREEN} ╰─➤  {C_CYAN}" + " ".join(map(str, args)) + C_DEF)

def nova_ask_user(prompt):
    return input(f"{C_YELL} ╰─➤  [INPUT] {prompt} {C_DEF}")

# Memory State
NOVA_ENV = {
    "Nova": type("NovaObj", (), {
        "show": nova_show,
        "ask": type("AskObj", (), {"user": nova_ask_user})()
    })(),
    "true": True,
    "false": False
}

def throw_error(err_type, details, snippet, fix):
    print(f"{C_RED}╭────────────────────────────────────────────────────────╮{C_DEF}")
    print(f"{C_RED}│ ❌ NOVA FATAL EXCEPTION                                │{C_DEF}")
    print(f"{C_RED}├────────────────────────────────────────────────────────┤{C_DEF}")
    print(f"{C_RED}│ Type    :{C_DEF} {C_YELL}{err_type}{C_DEF}")
    print(f"{C_RED}│ Details :{C_DEF} {details}")
    print(f"{C_RED}│ Snippet :{C_DEF} {C_CYAN}{snippet}{C_DEF}")
    print(f"{C_RED}│ Fix     :{C_DEF} {fix}")
    print(f"{C_RED}╰────────────────────────────────────────────────────────╯{C_DEF}")

def transpile_nova_to_py(code):
    # Syntax mapping (EBNF to Execution logic)
    code = re.sub(r'\btrue\b', 'True', code)
    code = re.sub(r'\bfalse\b', 'False', code)
    code = re.sub(r'Nova\.show\s*\(', 'Nova.show(', code)
    code = re.sub(r'Nova\.ask\.user\s*\(', 'Nova.ask.user(', code)
    
    lines = code.split('\n')
    out = []
    indent = 0
    for line in lines:
        s = line.strip()
        if not s: continue
        if s.endswith('{'):
            s = re.sub(r'^function\b', 'def', s)
            s = re.sub(r'^class\b', 'class', s)
            s = s[:-1].strip() + ":"
            out.append("    " * indent + s)
            indent += 1
        elif s.startswith('}'):
            indent -= 1
            if len(s) > 1:
                out.append("    " * indent + s[1:].strip())
        else:
            out.append("    " * indent + s)
    return "\n".join(out)

def execute_hacker_tool(tool, target):
    print(f"{C_CYAN}⚙️ [NovaArsenal] Routing '{tool}' via Silicon Bridge...{C_DEF}")
    time.sleep(0.5)
    tools = {
        "scan": f"nmap -F {target}",
        "sql": f"sqlmap -u {target}",
        "brute": f"hydra {target}",
        "who": f"whois {target}"
    }
    if tool in tools:
        print(f"  [*] Executing OS Bridge: {tools[tool]}")
        print(f"  {C_GREEN}╰─➤ Simulated Target Output / Execution Finished.{C_DEF}")
    else:
        print(f"  {C_RED}╰─➤ [!] Tool '{tool}' requires root NUPM mapping.{C_DEF}")

def run_repl():
    os.system('clear')
    print(f"{C_GREEN}")
    print(" ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗ ")
    print(" ████╗  ██║██╔═══██╗██║   ██║██╔══██╗")
    print(" ██╔██╗ ██║██║   ██║██║   ██║███████║")
    print(" ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║")
    print(" ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║")
    print(" ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝")
    print(f"{C_PURP}       Neura Studio | Architect: Javed{C_DEF}")
    print(f"{C_DARK}══════════════════════════════════════════════════════════════{C_DEF}")
    print(f"{C_CYAN} [©] Copyright 2026 Neura Studio. All Rights Reserved.{C_DEF}")
    print(f"{C_RED} [!] SECURE LINK: 500+ ARSENAL TOOLS & TRUE SYNTAX LOADED.{C_DEF}")
    print(f"{C_DARK}══════════════════════════════════════════════════════════════{C_DEF}")
    
    buffer = ""
    brackets = 0
    mode = "HACKER"

    while True:
        try:
            if brackets > 0:
                prompt = f"{C_DARK} ... {C_DEF}"
            else:
                prompt = f"{C_DARK}[{C_GREEN}NOVA:{mode}{C_DARK}] {C_ROOT}root@silicon{C_DEF} ⚡ "
            
            line = input(prompt)
            if line.strip() == "exit": break
            if line.strip() == "clear": 
                os.system('clear')
                continue
            
            if line.startswith("mode "):
                mode = line.split(" ")[1].upper()
                print(f"{C_GREEN} [+] Engine switched to {mode} mode.{C_DEF}")
                continue
                
            if line.startswith("run_tool "):
                parts = line.split(" ")
                tool = parts[1] if len(parts) > 1 else ""
                target = parts[2] if len(parts) > 2 else "(No Target)"
                execute_hacker_tool(tool, target)
                continue

            buffer += line + "\n"
            brackets += line.count('{') - line.count('}')
            
            if brackets <= 0 and buffer.strip():
                print(f"{C_DARK}--------------------------------------------------{C_DEF}")
                print(f"{C_DARK}--- Output ---{C_DEF}")
                
                py_code = transpile_nova_to_py(buffer)
                try:
                    # Try eval first for math/logic/single statements
                    res = eval(py_code, NOVA_ENV)
                    if res is not None:
                        if isinstance(res, bool):
                            res_str = "true" if res else "false"
                            color = C_GREEN if res else C_RED
                            print(f"{C_GREEN} ╰─➤  {color}{res_str}{C_DEF}")
                        else:
                            print(f"{C_GREEN} ╰─➤  {C_YELL}{res}{C_DEF}")
                except SyntaxError:
                    try:
                        # Try exec for assignments, loops, multi-line
                        exec(py_code, NOVA_ENV)
                        if "=" in buffer or "function" in buffer:
                            print(f"{C_DARK} ╰─➤  (Stored in Silicon Memory){C_DEF}")
                    except Exception as e:
                        throw_error(type(e).__name__, str(e), buffer.strip(), "Check syntax or variable declarations.")
                except Exception as e:
                    throw_error(type(e).__name__, str(e), buffer.strip(), "Check your mathematical logic or type casting.")
                
                print(f"{C_DARK}--------------------------------------------------{C_DEF}")
                buffer = ""
                brackets = 0
                
        except KeyboardInterrupt:
            buffer = ""
            brackets = 0
            print(f"\n{C_RED}[!] Process interrupted.{C_DEF}")
        except EOFError:
            break

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        # Simulate running a file
        print(f"{C_CYAN}Executing: {sys.argv[2]} natively on Silicon.{C_DEF}")
    else:
        run_repl()
