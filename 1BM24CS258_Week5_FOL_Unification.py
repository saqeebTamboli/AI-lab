def parse_expr(expr_str):
    """
    Parses a string representation of an expression into a list structure.
    Example: 'Eats(x, Apple)' -> ['Eats', 'x', 'Apple']
             'P(x, h(y))'    -> ['P', 'x', ['h', 'y']]
    """
    expr_str = expr_str.strip()
    if '(' not in expr_str:
        return expr_str
   
    pred_end = expr_str.index('(')
    pred = expr_str[:pred_end].strip()
    args_str = expr_str[pred_end + 1 : -1].strip()
   
    args = []
    current = []
    depth = 0
    for char in args_str:
        if char == ',' and depth == 0:
            args.append(parse_expr(''.join(current)))
            current = []
        else:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            current.append(char)
    if current:
        args.append(parse_expr(''.join(current)))
   
    return [pred] + args

def is_variable(term):
    """
    Checks if a term is a variable.
    By convention: single lowercase letter tokens (e.g., x, y, z) are variables.
    """
    return isinstance(term, str) and len(term) == 1 and term.islower()

def occurs_check(var, expr):
    """
    Returns True if variable `var` occurs anywhere within `expr`.
    """
    if var == expr:
        return True
    if isinstance(expr, list):
        return any(occurs_check(var, sub) for sub in expr)
    return False

def apply_subst(subst, expr):
    """
    Applies substitution dictionary `subst` recursively to expression `expr`.
    """
    if isinstance(expr, str):
        return subst.get(expr, expr)
    if isinstance(expr, list):
        return [apply_subst(subst, sub) for sub in expr]
    return expr

def unify(psi1, psi2):
    """
    Recursive Unification Algorithm for FOL expressions.
    """
    # Step 1: If psi1 or psi2 is a variable or constant (atom)
    if isinstance(psi1, str) or isinstance(psi2, str):
        if psi1 == psi2:
            return {}  # NIL (No substitution needed)
        elif is_variable(psi1):
            if occurs_check(psi1, psi2):
                return "FAILURE"
            return {psi1: psi2}
        elif is_variable(psi2):
            if occurs_check(psi2, psi1):
                return "FAILURE"
            return {psi2: psi1}
        else:
            return "FAILURE"

    # Step 2: Initial Predicate symbol check
    if psi1[0] != psi2[0]:
        return "FAILURE"

    # Step 3: Argument count check
    if len(psi1) != len(psi2):
        return "FAILURE"

    # Step 4: Set SUBST to NIL (empty dict)
    subst = {}

    # Step 5: Process arguments
    l1 = psi1[1:]
    l2 = psi2[1:]

    for i in range(len(l1)):
        # Step 5a: Unify i-th element of psi1 and psi2
        s = unify(l1[i], l2[i])

        # Step 5b: If unification fails
        if s == "FAILURE":
            return "FAILURE"

        # Step 5c: If S is not NIL
        if s:
            # Apply S to remaining terms
            l1 = [apply_subst(s, item) for item in l1]
            l2 = [apply_subst(s, item) for item in l2]
           
            # Update accumulated substitutions
            new_subst = {k: apply_subst(s, v) for k, v in subst.items()}
            new_subst.update(s)
            subst = new_subst

    # Step 6: Return substitution set
    return subst

def format_expr(parsed):
    """Converts a parsed expression list back to string format."""
    if isinstance(parsed, str):
        return parsed
    return f"{parsed[0]}({', '.join(format_expr(arg) for arg in parsed[1:])})"

def main():
    print("=== First-Order Logic (FOL) Unification Algorithm ===")
    print("Note: Single lowercase letters (e.g., x, y, z) are treated as variables.\n")

    e1_str = input("Enter Expression 1 (e.g., Eats(x, Apple)): ").strip()
    e2_str = input("Enter Expression 2 (e.g., Eats(Riya, y)): ").strip()

    psi1 = parse_expr(e1_str)
    psi2 = parse_expr(e2_str)

    result = unify(psi1, psi2)

    print("\n--- Output ---")
    if result == "FAILURE":
        print("Unification Result: FAILURE")
    else:
        print("Unification Result: SUCCESS")
        if not result:
            print("Substitutions: NIL (Expressions are already identical)")
        else:
            sub_strs = [f"{val}/{var}" for var, val in result.items()]
            print(f"Substitution Set (SUBST): {{ {', '.join(sub_strs)} }}")
           
            # Apply substitutions to get unified expression
            unified_psi1 = apply_subst(result, psi1)
            print(f"Unified Expression: {format_expr(unified_psi1)}")

if __name__ == "__main__":
    main()