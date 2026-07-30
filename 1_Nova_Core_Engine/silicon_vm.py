import re

class NovaRuntimeEngine:
    def __init__(self):
        self.variables = {}
        
    def expression_evaluator(self, expr):
        expr = str(expr).strip()
        
        # String Concatenation: "Welcome " + name
        if '+' in expr and ('"' in expr or "'" in expr):
            parts = expr.split('+')
            res = ""
            for p in parts:
                p = p.strip()
                if p.startswith('"') or p.startswith("'"):
                    res += p.strip("\"'")
                else:
                    res += str(self.variables.get(p, p))
            return res
            
        # Arithmetic: 20 + 30
        if any(op in expr for op in ['+', '-', '*', '/']) and not ('"' in expr or "'" in expr):
            try:
                safe_expr = expr
                for k, v in self.variables.items():
                    safe_expr = safe_expr.replace(k, str(v))
                return eval(safe_expr)
            except:
                pass
                
        # Direct Variable Lookup
        if expr in self.variables:
            return self.variables[expr]
            
        # Literals (Numbers, Raw Strings)
        if expr.isdigit() or expr.startswith('"') or expr.startswith("'"):
            return expr.strip("\"'")
            
        return None # Unresolved Variable
        
    def execute_function(self, func_name, args):
        clean_args = [self.expression_evaluator(a.strip()) for a in args]
        if func_name == "Add":
            return sum([int(a) for a in clean_args])
        return f"Executed {func_name}"
        
    def boolean_evaluator(self, condition):
        try:
            safe_cond = condition
            for k, v in self.variables.items():
                safe_cond = safe_cond.replace(k, str(v))
            return eval(safe_cond)
        except:
            return False
