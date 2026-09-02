from app.roulette import get_all_splits, get_splits_for_number


print("=== Split Test ===")

test_numbers = [0, 1, 2, 5, 17, 36]

for number in test_numbers:
    print(f"{number} -> {get_splits_for_number(number)}")


print("\n=== All Splits ===")

all_splits = get_all_splits()

for index, split in enumerate(all_splits, start=1):
    print(f"Split {index}: {split}")

print(f"\nTotal splits: {len(all_splits)}")