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


settings = APISettings()