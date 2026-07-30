import sys, re
from silicon_vm import NovaRuntimeEngine

vm = NovaRuntimeEngine()

def fatal_error(err_type, details, snippet):
    print("╭────────────────────────────────────────────────────────╮")
    print("│ ❌ NOVA FATAL EXCEPTION                                │")
    print("├────────────────────────────────────────────────────────┤")
    print(f"│ Type    : {err_type}")
    print(f"│ Details : {details}")
    print(f"│ Snippet : {snippet}")
    print("╰────────────────────────────────────────────────────────╯")
    sys.exit(1)

def run_script(filepath):
    print("⚙️ [SILICON_CORE] Booting Nova File Engine...")
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except Exception:
        sys.exit(1)

    i = 0
    skip_block = False

    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith('//'):
            i += 1
            continue

        if not line.startswith('}'):
            print("[COMPILER] ╰─➤  (Syntax Parsed & Mapped to VM in [Standard] Mode)")
            
        # Branch Executor Guard
        if skip_block:
            if line == '}':
                skip_block = False
            elif 'else {' in line:
                skip_block = False
            i += 1
            continue

        try:
            # 1. Imports
            if line.startswith('import '):
                match = re.search(r'import\s+Nova\.(\w+)', line)
                if match:
                    print(f"[MODULE_LOADER] ╰─➤ Module 'Nova.{match.group(1)}' loaded in [Standard] Mode RAM.")

            # 2. Input
            elif 'Nova.input' in line:
                match = re.search(r'let\s+(\w+)\s*=\s*Nova\.input\((.*?)\)', line)
                if match:
                    var_name = match.group(1)
                    prompt = vm.expression_evaluator(match.group(2))
                    val = input(f"[SYS_INPUT] ╰─➤  {prompt} : ")
                    vm.variables[var_name] = val
                    print(f"[RAM_ALLOC] ╰─➤  (Stored '{val}' in 0x{var_name.upper()})")

            # 3. Memory Allocation & Function Dispatcher
            elif line.startswith('let '):
                match = re.search(r'let\s+(\w+)\s*=\s*(.+)', line)
                if match:
                    var_name = match.group(1)
                    expr = match.group(2)
                    if '(' in expr and ')' in expr:
                        func = expr.split('(')[0].strip()
                        args = expr.split('(')[1].split(')')[0].split(',')
                        val = vm.execute_function(func, args)
                    else:
                        val = vm.expression_evaluator(expr)
                        
                    if val is None:
                        fatal_error("VariableNotFound", f"Variable '{expr}' is not mapped in Silicon RAM.", line)
                    vm.variables[var_name] = val
                    print(f"[RAM_ALLOC] ╰─➤  (Stored '{val}' in 0x{var_name.upper()})")

            # 4. Display Engine
            elif line.startswith('Nova.show'):
                match = re.search(r'Nova\.show\((.+)\)', line)
                if match:
                    expr = match.group(1)
                    val = vm.expression_evaluator(expr)
                    if val is None:
                        fatal_error("VariableNotFound", f"Variable '{expr}' is not mapped in Silicon RAM.", line)
                    print(f"[DATA_STREAM] ╰─➤  {val}")

            # 5. Boolean & Branching (if/else)
            elif line.startswith('if '):
                match = re.search(r'if\s+(.*?)\s*\{', line)
                if match:
                    if not vm.boolean_evaluator(match.group(1)):
                        skip_block = True
            elif line.startswith('else'):
                skip_block = True

            # 6. Iterator Engine (foreach)
            elif line.startswith('foreach '):
                match = re.search(r'foreach\s+(\w+)\s+in\s+(\w+)', line)
                if match:
                    iter_var = match.group(1)
                    collection_name = match.group(2)
                    if collection_name not in vm.variables:
                        fatal_error("VariableNotFound", f"Collection '{collection_name}' not found.", line)
                    vm.variables[iter_var] = vm.variables[collection_name][0] # Safe Scope Binding

            # 7. Exception Catch Binder
            elif line.startswith('catch '):
                match = re.search(r'catch\s+(\w+)', line)
                if match:
                    vm.variables[match.group(1)] = "Silicon Runtime Exception Object"

        except Exception as e:
            fatal_error("VMExecutionError", str(e), line)

        i += 1

    print("[✔] Execution Finished Safely.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_script(sys.argv[1])
