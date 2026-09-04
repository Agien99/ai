from app.database_service import DatabaseService
from app.session import RouletteSession


class SessionRepository:
    @staticmethod
    def create_session(session: RouletteSession) -> dict:
        query = """
            insert into public.sessions (
                session_id,
                status,
                initial_spin_count,
                started_at,
                ended_at,
                updated_at
            )
            values (%s, %s, %s, %s, %s, now())
            returning *
        """

        params = (
            session.session_id,
            session.status,
            len(session.initial_spins),
            session.started_at,
            session.ended_at,
        )

        result = DatabaseService.execute_returning_one(
            query,
            params,
        )

        if result is None:
            raise RuntimeError(
                "Failed to create session record."
            )

        return result

    @staticmethod
    def update_session(session: RouletteSession) -> None:
        query = """
            update public.sessions
            set
                status = %s,
                initial_spin_count = %s,
                started_at = %s,
                ended_at = %s,
                updated_at = now()
            where session_id = %s
        """

        params = (
            session.status,
            len(session.initial_spins),
            session.started_at,
            session.ended_at,
            session.session_id,
        )

        DatabaseService.execute(
            query,
            params,
        )

    @staticmethod
    def get_session(
        session_id: str,
    ) -> dict | None:
        query = """
            select
                session_id,
                status,
                initial_spin_count,
                started_at,
                ended_at,
                created_at,
                updated_at
            from public.sessions
            where session_id = %s
        """

        return DatabaseService.fetch_one(
            query,
            (session_id,),
        )

    @staticmethod
    def get_all_sessions() -> list[dict]:
        query = """
            select
                session_id,
                status,
                initial_spin_count,
                started_at,
                ended_at,
                created_at,
                updated_at
            from public.sessions
            order by started_at desc
        """

        return DatabaseService.fetch_all(query)