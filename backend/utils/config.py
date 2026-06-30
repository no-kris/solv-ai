import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(override=True)


def get_allowed_origins() -> list[str]:
    """
    Get allowed CORS origins from environment variable.
    Defaults to localhost if not set.
    Format: comma-separated URLs (e.g., "http://localhost:5173,http://127.0.0.1:5173")
    """
    origins_str = os.environ.get(
        "ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    )
    return [origin.strip() for origin in origins_str.split(",")]


def get_env(key: str) -> str:
    """
    Helper function for fetching environment variables.
    Raises RuntimeError if environment variable key is missing.
    """
    try:
        return os.environ[key]
    except KeyError:
        raise RuntimeError(f"Missing required environment variable: {key}")


@dataclass
class Config:
    __GROQ_API_KEY: str = get_env("GROQ_API_KEY")
    __GROQ_MODEL: str = get_env("GROQ_MODEL")
    __CLIENT = AsyncOpenAI(
        api_key=__GROQ_API_KEY, base_url="https://api.groq.com/openai/v1"
    )

    def get_client(self):
        return self.__CLIENT

    def get_model(self) -> str:
        return self.__GROQ_MODEL

    def __repr__(self) -> str:
        """
        String that get's printed when user calls print().
        """
        return "Not allowed to print config."


config = Config()
