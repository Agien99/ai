from datetime import datetime

from app.database_service import DatabaseService


class ModelMetricRepository:
    @staticmethod
    def create_model_metric(
        model_version_id: str,
        metric_scope: str,
        metric_name: str,
        metric_value: float,
        sample_count: int,
        evaluation_type: str,
        calculated_at: datetime | None = None,
    ) -> dict:
        query = """
            insert into public.model_metrics (
                model_version_id,
                metric_scope,
                metric_name,
                metric_value,
                sample_count,
                evaluation_type,
                calculated_at
            )
            values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                coalesce(%s, now())
            )
            returning *
        """

        result = DatabaseService.execute_returning_one(
            query,
            (
                model_version_id,
                metric_scope,
                metric_name,
                metric_value,
                sample_count,
                evaluation_type,
                calculated_at,
            ),
        )

        if result is None:
            raise RuntimeError(
                "Failed to create model metric."
            )

        return result

    @staticmethod
    def get_model_metrics(
        model_version_id: str,
    ) -> list[dict]:
        query = """
            select *
            from public.model_metrics
            where model_version_id = %s
            order by calculated_at asc
        """

        return DatabaseService.fetch_all(
            query,
            (model_version_id,),
        )

    @staticmethod
    def get_model_metrics_by_type(
        model_version_id: str,
        evaluation_type: str,
    ) -> list[dict]:
        query = """
            select *
            from public.model_metrics
            where model_version_id = %s
              and evaluation_type = %s
            order by calculated_at asc
        """

        return DatabaseService.fetch_all(
            query,
            (
                model_version_id,
                evaluation_type,
            ),
        )