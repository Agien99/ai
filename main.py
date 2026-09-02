from app.roulette import (
    get_main_grid_numbers,
    get_table_numbers,
    is_valid_number,
)


print("=== Roulette AI ===")

print("\nAll roulette numbers:")
print(get_table_numbers())

print("\nMain grid:")
print(get_main_grid_numbers())

print("\nValidation:")
print("17:", is_valid_number(17))
print("0:", is_valid_number(0))
print("36:", is_valid_number(36))
print("37:", is_valid_number(37))
print("-1:", is_valid_number(-1))