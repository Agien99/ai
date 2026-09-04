import os

from dotenv import load_dotenv


load_dotenv()


class APISettings:
    def __init__(self):
        self.api_title = os.getenv(
            "API_TITLE",
            "Roulette AI API",
        )

        self.api_version = os.getenv(
            "API_VERSION",
            "1.0.0",
        )

        self.api_environment = os.getenv(
            "API_ENV",
            "development",
        )

        cors_origins = os.getenv(
            "CORS_ORIGINS",
            (
                "http://localhost:5173,"
                "https://agien99.github.io"
            ),
        )

        self.cors_origins = [
            origin.strip()
            for origin
            in cors_origins.split(",")
            if origin.strip()
        ]


settings = APISettings()