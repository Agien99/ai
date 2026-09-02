# European Roulette contains numbers 0 to 36.
ROULETTE_NUMBERS = list(range(37))


def is_valid_number(number: int) -> bool:
    """
    Check whether a number is a valid European Roulette number.

    Valid numbers are 0 through 36.
    """
    return isinstance(number, int) and number in ROULETTE_NUMBERS


def get_table_numbers() -> list[int]:
    """
    Return all valid European Roulette numbers.
    """
    return ROULETTE_NUMBERS.copy()


def get_main_grid_numbers() -> list[int]:
    """
    Return the main roulette betting grid.

    Zero is excluded because dozens, columns, streets,
    splits, and corners are primarily based on numbers 1-36.
    """
    return list(range(1, 37))

def get_dozen(number: int) -> int | None:
    """
    Return the dozen for a roulette number.

    Returns:
        1 for numbers 1-12
        2 for numbers 13-24
        3 for numbers 25-36
        None for 0

    Raises:
        ValueError if the number is not a valid roulette number.
    """
    if not is_valid_number(number):
        raise ValueError(f"Invalid roulette number: {number}")

    if number == 0:
        return None

    if 1 <= number <= 12:
        return 1

    if 13 <= number <= 24:
        return 2

    return 3