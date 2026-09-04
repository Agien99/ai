from typing import Any

from psycopg.types.json import Jsonb

from app.database_service import DatabaseService


class PredictionItemRepository:
    @staticmethod
    def create_prediction_item(
        prediction_run_id: str,
        category: str,
        payload: Any,
    ) -> dict:
        query = """
            insert into public.prediction_items (
                prediction_run_id,
                category,
                payload
            )
            values (%s, %s, %s)
            returning *
        """

        result = DatabaseService.execute_returning_one(
            query,
            (
                prediction_run_id,
                category,
                Jsonb(payload),
            ),
        )

        if result is None:
            raise RuntimeError(
                "Failed to create prediction item."
            )

        return result

    @staticmethod
    def get_prediction_item(
        prediction_item_id: str,
    ) -> dict | None:
        query = """
            select *
            from public.prediction_items
            where prediction_item_id = %s
        """

        return DatabaseService.fetch_one(
            query,
            (prediction_item_id,),
        )

    @staticmethod
    def get_prediction_items(
        prediction_run_id: str,
    ) -> list[dict]:
        query = """
            select *
            from public.prediction_items
            where prediction_run_id = %s
            order by created_at asc
        """

        return DatabaseService.fetch_all(
            query,
            (prediction_run_id,),
        )

    @staticmethod
    def update_evaluation(
        prediction_item_id: str,
        is_hit: bool,
    ) -> dict:
        query = """
            update public.prediction_items
            set
                is_hit = %s,
                evaluated_at = now()
            where prediction_item_id = %s
            returning *
        """

        result = DatabaseService.execute_returning_one(
            query,
            (
                is_hit,
                prediction_item_id,
            ),
        )

        if result is None:
            raise ValueError(
                "Prediction item was not found."
            )

        return result