from datetime import datetime

from psycopg.types.json import Jsonb

from app.database_service import DatabaseService


class ModelVersionRepository:
    @staticmethod
    def get_all_model_versions(
    ) -> list[dict]:
        query = """
            select *
            from public.model_versions
            order by
                model_name asc,
                version_number desc
        """

        return DatabaseService.fetch_all(
            query
        )

    @staticmethod
    def create_model_version(
        model_name: str,
        version_number: int,
        feature_version: str,
        training_row_count: int,
        training_session_count: int | None = None,
        training_parameters: dict | None = None,
        artifact_path: str | None = None,
        is_active: bool = False,
        trained_at: datetime | None = None,
    ) -> dict:
        query = """
            insert into public.model_versions (
                model_name,
                version_number,
                feature_version,
                training_row_count,
                training_session_count,
                training_parameters,
                artifact_path,
                is_active,
                trained_at
            )
            values (
                %s,
                %s,
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

        parameters = (
            Jsonb(training_parameters)
            if training_parameters is not None
            else None
        )

        result = DatabaseService.execute_returning_one(
            query,
            (
                model_name,
                version_number,
                feature_version,
                training_row_count,
                training_session_count,
                parameters,
                artifact_path,
                is_active,
                trained_at,
            ),
        )

        if result is None:
            raise RuntimeError(
                "Failed to create model version."
            )

        return result

    @staticmethod
    def get_model_version(
        model_version_id: str,
    ) -> dict | None:
        query = """
            select *
            from public.model_versions
            where model_version_id = %s
        """

        return DatabaseService.fetch_one(
            query,
            (model_version_id,),
        )

    @staticmethod
    def get_model_versions(
        model_name: str,
    ) -> list[dict]:
        query = """
            select *
            from public.model_versions
            where model_name = %s
            order by version_number desc
        """

        return DatabaseService.fetch_all(
            query,
            (model_name,),
        )

    @staticmethod
    def get_active_model_version(
        model_name: str,
    ) -> dict | None:
        query = """
            select *
            from public.model_versions
            where model_name = %s
              and is_active = true
            order by version_number desc
            limit 1
        """

        return DatabaseService.fetch_one(
            query,
            (model_name,),
        )

    @staticmethod
    def deactivate_model_versions(
        model_name: str,
    ) -> None:
        query = """
            update public.model_versions
            set is_active = false
            where model_name = %s
              and is_active = true
        """

        DatabaseService.execute(
            query,
            (model_name,),
        )

    @staticmethod
    def activate_model_version(
        model_version_id: str,
    ) -> None:
        query = """
            update public.model_versions
            set is_active = true
            where model_version_id = %s
        """

        DatabaseService.execute(
            query,
            (model_version_id,),
        )