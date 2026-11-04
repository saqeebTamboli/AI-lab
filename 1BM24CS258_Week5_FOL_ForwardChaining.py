
def is_variable(term):
    """Single character lowercase names are variables (e.g., x, y, z)."""
    return isinstance(term, str) and len(term) == 1 and term.islower()

def match_term(rule_term, fact_term, subst):
    """Matches a term (predicate/argument) from a rule with a fact given current substitutions."""
    if is_variable(rule_term):
        if rule_term in subst:
            return subst if subst[rule_term] == fact_term else None
        else:
            new_subst = subst.copy()
            new_subst[rule_term] = fact_term
            return new_subst
    elif rule_term == fact_term:
        return subst
    return None

def match_atom(rule_atom, fact_atom, subst):
    """Matches an atomic sentence like ('Missile', 'x') with ('Missile', 'M1')."""
    if rule_atom[0] != fact_atom[0] or len(rule_atom) != len(fact_atom):
        return None
   
    current_subst = subst.copy()
    for r_arg, f_arg in zip(rule_atom[1:], fact_atom[1:]):
        res = match_term(r_arg, f_arg, current_subst)
        if res is None:
            return None
        current_subst = res
    return current_subst

def match_premises(premises, facts, subst):
    """Finds all substitutions matching a list of premises against KB facts."""
    if not premises:
        yield subst
        return
   
    first = premises[0]
    rest = premises[1:]
   
    for fact in facts:
        res = match_atom(first, fact, subst)
        if res is not None:
            yield from match_premises(rest, facts, res)

def apply_subst_to_atom(atom, subst):
    """Applies substitution dictionary to an atomic sentence tuple."""
    return tuple(subst.get(arg, arg) if is_variable(arg) else arg for arg in atom)

class FOLKnowledgeBase:
    def __init__(self):
        self.facts = []   # List of tuples: e.g., ('American', 'West')
        self.rules = []   # List of dicts: {'premises': [...], 'conclusion': (...)}

    def add_fact(self, fact_tuple):
        if fact_tuple not in self.facts:
            self.facts.append(fact_tuple)

    def add_rule(self, premises, conclusion):
        self.rules.append({'premises': premises, 'conclusion': conclusion})

    def forward_chain(self, query):
        print("==================================================")
        print("          STARTING FORWARD REASONING             ")
        print("==================================================")
       
        iteration = 1
        proof_tree = []

        while True:
            print(f"\n--- Iteration {iteration} ---")
            new_facts = []

            for rule in self.rules:
                premises = rule['premises']
                conclusion = rule['conclusion']

                # Find all valid substitutions matching premises to current facts
                for subst in match_premises(premises, self.facts, {}):
                    inferred_fact = apply_subst_to_atom(conclusion, subst)
                   
                    if inferred_fact not in self.facts and inferred_fact not in new_facts:
                        new_facts.append(inferred_fact)
                       
                        # Format premises for proof logging
                        matched_premises = [apply_subst_to_atom(p, subst) for p in premises]
                        log_entry = f"Inferred {format_atom(inferred_fact)} from rule premises {matched_premises} using θ={subst}"
                        proof_tree.append(log_entry)
                        print(f"[+] {log_entry}")

                        # Check if query derived
                        if inferred_fact == query:
                            print("\n==================================================")
                            print(f"SUCCESS: Query {format_atom(query)} PROVEN!")
                            print("==================================================")
                            return True, proof_tree

            if not new_facts:
                print("\n[!] No new facts derived in this iteration.")
                break

            self.facts.extend(new_facts)
            iteration += 1

        print("\n==================================================")
        print(f"FAILURE: Query {format_atom(query)} CANNOT be proven.")
        print("==================================================")
        return False, proof_tree

def format_atom(atom):
    """Formats atom tuple back to FOL string representation."""
    return f"{atom[0]}({', '.join(atom[1:])})"

def load_crime_case_study(kb):
    """Loads Colonel West / Crime case study rules and facts into Knowledge Base."""
    # Facts
    kb.add_fact(('American', 'West'))
    kb.add_fact(('Enemy', 'Nono', 'America'))
    kb.add_fact(('Owns', 'Nono', 'M1'))
    kb.add_fact(('Missile', 'M1'))

    # Rule 1: Missile(x) => Weapon(x)
    kb.add_rule([('Missile', 'x')], ('Weapon', 'x'))
   
    # Rule 2: Enemy(x, America) => Hostile(x)
    kb.add_rule([('Enemy', 'x', 'America')], ('Hostile', 'x'))

    # Rule 3: Missile(x) AND Owns(Nono, x) => Sells(West, x, Nono)
    kb.add_rule([('Missile', 'x'), ('Owns', 'Nono', 'x')], ('Sells', 'West', 'x', 'Nono'))

    # Rule 4: American(x) AND Weapon(y) AND Sells(x, y, z) AND Hostile(z) => Criminal(x)
    kb.add_rule(
        [('American', 'x'), ('Weapon', 'y'), ('Sells', 'x', 'y', 'z'), ('Hostile', 'z')],
        ('Criminal', 'x')
    )

def main():
    kb = FOLKnowledgeBase()
   
    print("=== First-Order Logic Forward Chaining Engine ===")
    print("1. Run Standard Case Study ('Is Colonel West a Criminal?')")
    print("2. Enter Custom Knowledge Base")
    choice = input("Enter choice (1/2): ").strip()

    if choice == '1':
        load_crime_case_study(kb)
        query = ('Criminal', 'West')
    else:
        num_facts = int(input("\nEnter number of initial facts: "))
        for i in range(num_facts):
            fact_str = input(f"Fact {i+1} (e.g. American West or Owns Nono M1): ").strip().split()
            kb.add_fact(tuple(fact_str))

        num_rules = int(input("\nEnter number of rules: "))
        for i in range(num_rules):
            print(f"\nRule {i+1}:")
            p_count = int(input("  Number of premises: "))
            premises = []
            for j in range(p_count):
                p_tokens = input(f"    Premise {j+1} (space-separated, e.g., Missile x): ").strip().split()
                premises.append(tuple(p_tokens))
            c_tokens = input("  Conclusion (e.g., Weapon x): ").strip().split()
            kb.add_rule(premises, tuple(c_tokens))

        q_tokens = input("\nEnter Query to Prove (e.g., Criminal West): ").strip().split()
        query = tuple(q_tokens)

    print("\nInitial Knowledge Base Facts:")
    for f in kb.facts:
        print(" -", format_atom(f))

    success, proof = kb.forward_chain(query)
   
    if success:
        print("\n--- DERIVED PROOF TREE STEPS ---")
        for step in proof:
            print(" ->", step)

if __name__ == "__main__":
    main()