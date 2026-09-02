from app.roulette import (
    get_all_corners,
    get_corners_for_number,
)


print("=== Corner Test ===")

test_numbers = [0, 1, 2, 5, 17, 36]

for number in test_numbers:
    print(f"{number} -> {get_corners_for_number(number)}")


print("\n=== All Corners ===")

all_corners = get_all_corners()

for index, corner in enumerate(all_corners, start=1):
    print(f"Corner {index}: {corner}")

print(f"\nTotal corners: {len(all_corners)}")