from datetime import datetime

from app.database_service import DatabaseService


class SpinRepository:
    @staticmethod
    def create_spin(
        session_id: str,
        spin_index: int,
        number: int,
        spin_type: str,
        spun_at: datetime | None = None,
    ) -> dict:
        query = """
            insert into public.spins (
                session_id,
                spin_index,
                number,
                spin_type,
                spun_at
            )
            values (%s, %s, %s, %s, %s)
            returning *
        """

        result = DatabaseService.execute_returning_one(
            query,
            (
                session_id,
                spin_index,
                number,
                spin_type,
                spun_at,
            ),
        )

        if result is None:
            raise RuntimeError(
                "Failed to create spin record."
            )

        return result

    @staticmethod
    def get_spin(
        spin_id: str,
    ) -> dict | None:
        query = """
            select *
            from public.spins
            where spin_id = %s
        """

        return DatabaseService.fetch_one(
            query,
            (spin_id,),
        )

    @staticmethod
    def get_spin_by_index(
        session_id: str,
        spin_index: int,
    ) -> dict | None:
        query = """
            select *
            from public.spins
            where session_id = %s
              and spin_index = %s
        """

        return DatabaseService.fetch_one(
            query,
            (
                session_id,
                spin_index,
            ),
        )

    @staticmethod
    def get_session_spins(
        session_id: str,
    ) -> list[dict]:
        query = """
            select
                spin_id,
                session_id,
                spin_index,
                number,
                spin_type,
                spun_at,
                created_at
            from public.spins
            where session_id = %s
            order by spin_index asc
        """

        return DatabaseService.fetch_all(
            query,
            (session_id,),
        )