from app.roulette import get_dozen


print("=== Dozen Test ===")

test_numbers = [0, 1, 12, 13, 24, 25, 36]

for number in test_numbers:
    print(f"{number} -> Dozen {get_dozen(number)}")