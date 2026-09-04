import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


class DatabaseConfig:
    @staticmethod
    def get_database_url() -> str:
        database_url = os.getenv("DATABASE_URL")

        if not database_url:
            raise ValueError(
                "DATABASE_URL environment variable is not configured."
            )

        return database_url

    @staticmethod
    def get_connection():
        database_url = DatabaseConfig.get_database_url()

        return psycopg.connect(database_url)