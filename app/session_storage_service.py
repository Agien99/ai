from app.session import RouletteSession
from app.session_repository import SessionRepository
from app.spin_repository import SpinRepository


class SessionStorageService:
    @staticmethod
    def load_session(
        session_id: str,
    ) -> RouletteSession | None:
        session_row = SessionRepository.get_session(
            session_id
        )

        if session_row is None:
            return None

        spin_rows = SpinRepository.get_session_spins(
            session_id
        )

        session = RouletteSession()

        # Restore persisted identity and timestamps.
        session.session_id = str(
            session_row["session_id"]
        )
        session.status = session_row["status"]
        session.started_at = session_row[
            "started_at"
        ]
        session.ended_at = session_row[
            "ended_at"
        ]

        spins = [
            row["number"]
            for row in spin_rows
        ]

        initial_spin_count = session_row[
            "initial_spin_count"
        ]

        session.initial_spins = spins[
            :initial_spin_count
        ]

        session.spins = spins

        return session

    @staticmethod
    def load_all_sessions(
    ) -> list[RouletteSession]:
        session_rows = (
            SessionRepository.get_all_sessions()
        )

        sessions = []

        for row in session_rows:
            session = (
                SessionStorageService.load_session(
                    str(row["session_id"])
                )
            )

            if session is not None:
                sessions.append(session)

        return sessions