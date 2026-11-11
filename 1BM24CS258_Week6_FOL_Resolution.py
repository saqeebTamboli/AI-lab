# Knowledge Base in CNF
KB = {
    "C1": "~food(x) | likes(John,x)",
    "C2": "food(Apple)",
    "C3": "food(Vegetables)",
    "C4": "~eats(y,z) | killed(y) | food(z)",
    "C5": "eats(Anil,Peanuts)",
    "C6": "alive(Anil)",
    "C7": "~eats(Anil,w) | eats(Harry,w)",
    "C8": "killed(g) | alive(g)",
    "C9": "~alive(k) | ~killed(k)"
}

query = "likes(John,Peanuts)"

print("KNOWLEDGE BASE:")
for key, value in KB.items():
    print(f"{key}: {value}")

print("\nQuery:", query)
print("Negated Query: ~" + query)

# Resolution proof steps
steps = [
    ("~likes(John,Peanuts)",
     "~food(x) | likes(John,x)",
     "~food(Peanuts)"),

    ("~food(Peanuts)",
     "~eats(y,z) | killed(y) | food(z)",
     "~eats(y,Peanuts) | killed(y)"),

    ("~eats(y,Peanuts) | killed(y)",
     "eats(Anil,Peanuts)",
     "killed(Anil)"),

    ("killed(Anil)",
     "~alive(k) | ~killed(k)",
     "~alive(Anil)"),

    ("~alive(Anil)",
     "alive(Anil)",
     "{}")
]

print("\nRESOLUTION STEPS:")
for i, (left, right, result) in enumerate(steps, 1):
    print(f"\nStep {i}:")
    print(" Clause 1:", left)
    print(" Clause 2:", right)
    print(" Resolvent:", result)

print("\nRESOLUTION PROOF TREE")
print("-" * 50)

for left, right, result in steps:
    print(f"\n{left} + {right}")
    print(" |")
    print(" v")
    print(f" {result}")

print("\n" + "=" * 50)

if steps[-1][2] == "{}":
    print("Empty clause obtained!")
    print("RESULT: John likes Peanuts.")
    print("Hence Proved.")
else:
    print("Proof unsuccessful.")
