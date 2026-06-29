import random

def attack(attacker, defender):
    move = random.choice([
        ("Takedown", 2),
        ("Reversal", 1),
        ("Escape", 1),
        ("Push Out", 1)
    ])

    name, points = move

    attack_roll = random.randint(1, 10) + attacker["skill"]
    defense_roll = random.randint(1, 10) + defender["skill"]

    print(f"\n{attacker['name']} attempts {name}!")

    if attack_roll > defense_roll:
        attacker["score"] += points
        print(f"✔ Success! +{points} points")
    else:
        print("✖ Failed attempt")

def show_score(a, b):
    print("\n--- SCORE ---")
    print(f"{a['name']}: {a['score']}")
    print(f"{b['name']}: {b['score']}")

def create_wrestler(name):
    return {
        "name": name,
        "skill": random.randint(1, 10),
        "score": 0
    }

print("=== OLYMPIC WRESTLING MATCH ===")

p1 = create_wrestler(input("Wrestler 1 name: "))
p2 = create_wrestler(input("Wrestler 2 name: "))

rounds = 6

for r in range(1, rounds + 1):
    print(f"\n===== ROUND {r} =====")

    attack(p1, p2)
    attack(p2, p1)

    show_score(p1, p2)

    # tech fall rule
    if p1["score"] >= 10 or p2["score"] >= 10:
        print("\n🏆 TECHNICAL FALL!")
        break

# decide winner
if p1["score"] > p2["score"]:
    winner = p1["name"]
elif p2["score"] > p1["score"]:
    winner = p2["name"]
else:
    winner = "DRAW"

print("\n🏆 MATCH OVER")
print("Winner:", winner)