from itertools import product


# Implication: A -> B is equivalent to (not A) or B
def implies(a, b):
    return (not a) or b


# Knowledge base: (Q -> P) AND (P -> NOT Q) AND (Q OR R)
def KB(P, Q, R):
    return (
        implies(Q, P)
        and implies(P, not Q)
        and (Q or R)
    )


# Truth-table enumeration for entailment
def entails(query):
    symbols = [True, False]

    for P, Q, R in product(symbols, repeat=3):
        kb_value = KB(P, Q, R)
        query_value = query(P, Q, R)

        # A counterexample: KB is true but query is false
        if kb_value and not query_value:
            return False

    return True


# Display the complete truth table
print("P Q R | Q->P P->~Q Q|R | KB")

for P, Q, R in product([True, False], repeat=3):
    a = implies(Q, P)
    b = implies(P, not Q)
    c = Q or R
    kb_value = KB(P, Q, R)

    def tf(value):
        return "T" if value else "F"

    print(
        tf(P), tf(Q), tf(R), "|",
        tf(a), "   ", tf(b), " ", tf(c), "|",
        tf(kb_value)
    )

print("\nKB entails R:", entails(lambda P, Q, R: R))

print(
    "KB entails (R -> P):",
    entails(lambda P, Q, R: implies(R, P))
)

print(
    "KB entails (Q -> R):",
    entails(lambda P, Q, R: implies(Q, R))
)
