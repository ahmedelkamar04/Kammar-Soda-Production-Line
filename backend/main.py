import random
import time

produced = 0
defective = 0

print("================================")
print(" Soda Bottle Production Line ")
print("================================")

while produced < 50:
    produced += 1
    print(f"\nBottle #{produced}")

    print("1. Empty bottle created")
    time.sleep(0.2)

    print("2. Bottle filled with soda")
    time.sleep(0.2)

    print("3. CO2 carbonation added")
    time.sleep(0.2)

    print("4. Cap placed")
    time.sleep(0.2)

    print("5. Label placed")
    time.sleep(0.2)

    defect_reason = random.choice([
        "None",
        "Underfilled bottle",
        "Missing cap",
        "Missing label",
        "Low carbonation"
    ])

    if defect_reason == "None":
        print("6. Quality check passed")
        print("Finished bottle accepted")
    else:
        defective += 1
        print("6. Quality check failed")
        print("Defect reason:", defect_reason)

    print("Total produced:", produced)
    print("Total defective:", defective)

    time.sleep(0.5)
    
