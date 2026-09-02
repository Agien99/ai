from app.roulette import (
    validate_initial_history,
    validate_spin_history,
)


print("=== Validation Test ===")


valid_history = [
    12, 7, 31, 4, 18,
    22, 9, 14, 0, 27,
    6, 33,
]

print("Valid history:")
print(valid_history)

print(
    "Spin history valid:",
    validate_spin_history(valid_history)
)

print(
    "Initial history valid:",
    validate_initial_history(valid_history)
)