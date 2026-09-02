from datetime import datetime
from uuid import uuid4

from app.roulette import is_valid_number, validate_initial_history


class RouletteSession:
    """
    Represents one continuous roulette observation session.
    """

    def __init__(self):
        self.session_id = str(uuid4())
        self.status = "NEW"

        self.initial_spins = []
        self.spins = []

        self.started_at = datetime.now()
        self.ended_at = None

    def start(self, initial_spins: list[int]):
        """
        Start the session using 10-15 recent roulette results.
        """
        if self.status != "NEW":
            raise ValueError("Session has already been started.")

        validate_initial_history(initial_spins)

        self.initial_spins = initial_spins.copy()
        self.spins = initial_spins.copy()

        self.status = "ACTIVE"

    def add_spin(self, number: int):
        """
        Add one new roulette result to an active session.
        """
        if self.status != "ACTIVE":
            raise ValueError(
                "Cannot add spin to a session that is not active."
            )

        if not is_valid_number(number):
            raise ValueError(f"Invalid roulette number: {number}")

        self.spins.append(number)

    def get_spin_sequence(self) -> list[tuple[int, int]]:
        """
        Return all spins together with their sequence number.
        """
        return [
            (index, number)
            for index, number in enumerate(self.spins, start=1)
        ]

    def __repr__(self):
        return (
            f"RouletteSession("
            f"session_id='{self.session_id}', "
            f"status='{self.status}', "
            f"spin_count={len(self.spins)}"
            f")"
        )