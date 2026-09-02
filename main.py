from app.roulette import get_column


print("=== Column Test ===")

test_numbers = [
    0,
    1, 2, 3,
    4, 5, 6,
    34, 35, 36,
]

for number in test_numbers:
    print(f"{number} -> Column {get_column(number)}")