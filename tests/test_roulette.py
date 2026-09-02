from app.roulette import (
    get_all_corners,
    get_all_splits,
    get_all_streets,
    get_column,
    get_corners_for_number,
    get_dozen,
    get_splits_for_number,
    get_street,
    is_valid_number,
    validate_initial_history,
    validate_spin_history,
)


def test_valid_roulette_numbers():
    assert is_valid_number(0) is True
    assert is_valid_number(17) is True
    assert is_valid_number(36) is True

    assert is_valid_number(-1) is False
    assert is_valid_number(37) is False
    assert is_valid_number(100) is False


def test_dozens():
    assert get_dozen(0) is None

    assert get_dozen(1) == 1
    assert get_dozen(12) == 1

    assert get_dozen(13) == 2
    assert get_dozen(24) == 2

    assert get_dozen(25) == 3
    assert get_dozen(36) == 3


def test_columns():
    assert get_column(0) is None

    assert get_column(1) == 1
    assert get_column(34) == 1

    assert get_column(2) == 2
    assert get_column(35) == 2

    assert get_column(3) == 3
    assert get_column(36) == 3


def test_streets():
    assert get_street(0) is None

    assert get_street(1) == (1, 2, 3)
    assert get_street(3) == (1, 2, 3)

    assert get_street(17) == (16, 17, 18)

    assert get_street(34) == (34, 35, 36)
    assert get_street(36) == (34, 35, 36)

    assert len(get_all_streets()) == 12


def test_splits():
    splits = get_all_splits()

    assert len(splits) == 57

    assert (1, 2) in splits
    assert (2, 3) in splits

    assert (1, 4) in splits
    assert (33, 36) in splits

    assert (1, 2) in get_splits_for_number(1)
    assert (1, 4) in get_splits_for_number(1)

    assert get_splits_for_number(0) == []


def test_corners():
    corners = get_all_corners()

    assert len(corners) == 22

    assert (1, 2, 4, 5) in corners
    assert (2, 3, 5, 6) in corners
    assert (32, 33, 35, 36) in corners

    assert (1, 2, 4, 5) in get_corners_for_number(1)

    assert get_corners_for_number(0) == []


def test_spin_history_validation():
    valid_history = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    assert validate_spin_history(valid_history) is True


def test_initial_history_validation():
    valid_history = [
        12, 7, 31, 4, 18,
        22, 9, 14, 0, 27,
    ]

    assert validate_initial_history(valid_history) is True