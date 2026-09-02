from app.roulette import get_all_streets, get_street


print("=== Street Test ===")

test_numbers = [0, 1, 3, 4, 5, 6, 7, 17, 34, 36]

for number in test_numbers:
    print(f"{number} -> {get_street(number)}")


print("\n=== All Streets ===")

for index, street in enumerate(get_all_streets(), start=1):
    print(f"Street {index}: {street}")