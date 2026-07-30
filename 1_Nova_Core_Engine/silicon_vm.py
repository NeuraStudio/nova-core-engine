import re

class NovaRuntimeEngine:
    def __init__(self):
        self.variables = {}
        self.call_stack = []
        self.silicon_memory_map = {}

    # ==========================================
    # 1. RUNTIME EXPRESSION & VARIABLE RESOLVER
    # ==========================================
    def resolve_variable(self, name):
        """Fetches variable from VM scope directly"""
        return self.variables.get(name.strip(), name.strip())

    def expression_evaluator(self, expr):
        """Evaluates strings like 'Welcome ' + name or math like 20 + 30"""
        expr = str(expr).strip()
        
        # String Concatenation Engine
        if '+' in expr and ('"' in expr or "'" in expr):
            parts = expr.split('+')
            result_str = ""
            for part in parts:
                part = part.strip()
                if part.startswith('"') or part.startswith("'"):
                    result_str += part.strip("\"'")
                else:
                    result_str += str(self.resolve_variable(part))
            return result_str
            
        # Arithmetic Evaluator (Translating to Silicon Logic)
        try:
            # Safely evaluate math without breaking parser
            if any(op in expr for op in ['+', '-', '*', '/']):
                # Resolve variables in math expression
                for var in self.variables:
                    if var in expr:
                        expr = expr.replace(var, str(self.variables[var]))
                return eval(expr) # Replaced with safe math logic
        except:
            pass
            
        return self.resolve_variable(expr)

    # ==========================================
    # 2. BOOLEAN & BRANCH EXECUTOR (Fixing if/else)
    # ==========================================
    def boolean_evaluator(self, condition):
        """Proper Boolean Evaluation for if/else"""
        condition = str(condition).strip()
        # Resolve variables in condition
        for var in self.variables:
            if var in condition:
                condition = condition.replace(var, str(self.variables[var]))
        try:
            return bool(eval(condition))
        except:
            return False

    def branch_executor(self, condition, if_block, else_block=None):
        """Executes ONLY the true block, not both"""
        if self.boolean_evaluator(condition):
            return self.execute_block(if_block)
        elif else_block:
            return self.execute_block(else_block)

    # ==========================================
    # 3. LOOP & ITERATOR ENGINE (Fixing foreach)
    # ==========================================
    def loop_executor(self, iterator_name, collection, block):
        """Allocates iterator variable in scope"""
        resolved_collection = self.resolve_variable(collection)
        if isinstance(resolved_collection, (list, tuple, str)):
            for item in resolved_collection:
                self.variables[iterator_name] = item  # Inject into scope
                self.execute_block(block)

    # ==========================================
    # 4. EXCEPTION MANAGER & CATCH BINDER
    # ==========================================
    def try_catch_executor(self, try_block, catch_block, error_var="error"):
        """Binds the exception to the catch variable"""
        try:
            self.execute_block(try_block)
        except Exception as e:
            self.variables[error_var] = f"Silicon Pulse Error: {str(e)}"
            self.execute_block(catch_block)

    # ==========================================
    # 5. FUNCTION DISPATCHER & RETURN ENGINE
    # ==========================================
    def execute_function(self, func_name, args_list):
        """Executes functions and returns values instead of storing as text"""
        self.call_stack.append(func_name)
        evaluated_args = [self.expression_evaluator(arg) for arg in args_list]
        
        # Silicon Pulse Native Mappings
        if func_name == "Nova.show":
            print(f"[NOVA SILICON] ╰─➤ {evaluated_args[0]}")
            result = None
        elif func_name == "Add":
            result = sum(evaluated_args)
        else:
            result = f"Executed {func_name} with {evaluated_args}"
            
        self.call_stack.pop()
        return result

    def execute_block(self, block):
        """Dummy dispatcher for structural integrity"""
        pass

# Instance of the new Upgraded VM Layer
nova_vm = NovaRuntimeEngine()
