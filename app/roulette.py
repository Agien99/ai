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

def get_column(number: int) -> int | None:
    """
    Return the roulette column for a number.

    Returns:
        1 for Column 1
        2 for Column 2
        3 for Column 3
        None for 0

    Raises:
        ValueError if the number is not a valid roulette number.
    """
    if not is_valid_number(number):
        raise ValueError(f"Invalid roulette number: {number}")

    if number == 0:
        return None

    remainder = number % 3

    if remainder == 1:
        return 1

    if remainder == 2:
        return 2

    return 3

def get_street(number: int) -> tuple[int, int, int] | None:
    """
    Return the street containing the given roulette number.

    Example:
        1 -> (1, 2, 3)
        5 -> (4, 5, 6)
        36 -> (34, 35, 36)

    Returns:
        A tuple of 3 numbers representing the street.
        None for 0.

    Raises:
        ValueError if the number is invalid.
    """
    if not is_valid_number(number):
        raise ValueError(f"Invalid roulette number: {number}")

    if number == 0:
        return None

    start = ((number - 1) // 3) * 3 + 1

    return (start, start + 1, start + 2)

def get_all_streets() -> list[tuple[int, int, int]]:
    """
    Return all 12 standard street bets.
    """
    return [
        (start, start + 1, start + 2)
        for start in range(1, 37, 3)
    ]

def get_all_splits() -> list[tuple[int, int]]:
    """
    Return all standard split bets for numbers 1-36.

    Includes:
        - Horizontal splits
        - Vertical splits
    """
    splits = []

    # Horizontal splits
    # Example: (1, 2), (2, 3), (4, 5), (5, 6)
    for row_start in range(1, 37, 3):
        splits.append((row_start, row_start + 1))
        splits.append((row_start + 1, row_start + 2))

    # Vertical splits
    # Example: (1, 4), (2, 5), (3, 6)
    for number in range(1, 34):
        splits.append((number, number + 3))

    return splits

def get_splits_for_number(number: int) -> list[tuple[int, int]]:
    """
    Return all standard split bets containing the given number.

    Returns:
        A list of split tuples.

    Raises:
        ValueError if the number is invalid.
    """
    if not is_valid_number(number):
        raise ValueError(f"Invalid roulette number: {number}")

    if number == 0:
        return []

    return [
        split
        for split in get_all_splits()
        if number in split
    ]