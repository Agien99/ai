from app.database_service import DatabaseService


class PredictionRunRepository:
    @staticmethod
    def get_latest_prediction_run(
        session_id: str,
    ) -> dict | None:
        query = """
            select *
            from public.prediction_runs
            where session_id = %s
            order by generated_at desc
            limit 1
        """

        return DatabaseService.fetch_one(
            query,
            (session_id,),
        )

    @staticmethod
    def create_prediction_run(
        session_id: str,
        strategy_key: str,
        prediction_for_spin_index: int,
        input_spin_count: int,
        recent_window: int | None = None,
        model_version_id: str | None = None,
    ) -> dict:
        query = """
            insert into public.prediction_runs (
                session_id,
                model_version_id,
                strategy_key,
                prediction_for_spin_index,
                input_spin_count,
                recent_window,
                generated_at
            )
            values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                now()
            )
            returning *
        """

        result = DatabaseService.execute_returning_one(
            query,
            (
                session_id,
                model_version_id,
                strategy_key,
                prediction_for_spin_index,
                input_spin_count,
                recent_window,
            ),
        )

        if result is None:
            raise RuntimeError(
                "Failed to create prediction run."
            )

        return result

    @staticmethod
    def get_prediction_run(
        prediction_run_id: str,
    ) -> dict | None:
        query = """
            select *
            from public.prediction_runs
            where prediction_run_id = %s
        """

        return DatabaseService.fetch_one(
            query,
            (prediction_run_id,),
        )

    @staticmethod
    def get_session_prediction_runs(
        session_id: str,
    ) -> list[dict]:
        query = """
            select *
            from public.prediction_runs
            where session_id = %s
            order by generated_at asc
        """

        return DatabaseService.fetch_all(
            query,
            (session_id,),
        )

    @staticmethod
    def evaluate_prediction_run(
        prediction_run_id: str,
        actual_spin_id: str,
    ) -> dict:
        query = """
            update public.prediction_runs
            set
                actual_spin_id = %s,
                evaluated_at = now()
            where prediction_run_id = %s
            returning *
        """

        result = DatabaseService.execute_returning_one(
            query,
            (
                actual_spin_id,
                prediction_run_id,
            ),
        )

        if result is None:
            raise ValueError(
                "Prediction run was not found."
            )

        return result