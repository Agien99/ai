from datetime import datetime
from uuid import uuid4


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

    def __repr__(self):
        return (
            f"RouletteSession("
            f"session_id='{self.session_id}', "
            f"status='{self.status}', "
            f"spin_count={len(self.spins)}"
            f")"
        )