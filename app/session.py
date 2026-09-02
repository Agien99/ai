from datetime import datetime
from uuid import uuid4

from app.roulette import validate_initial_history


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

    def __repr__(self):
        return (
            f"RouletteSession("
            f"session_id='{self.session_id}', "
            f"status='{self.status}', "
            f"spin_count={len(self.spins)}"
            f")"
        )