import os
from dataclasses import dataclass

from dotenv import load_dotenv
from huggingface_hub import AsyncInferenceClient

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
    __HF_TOKEN: str = get_env("HF_TOKEN")
    __MODEL: str = get_env("MODEL")
    __CLIENT = AsyncInferenceClient(token=__HF_TOKEN)

    def get_client(self) -> AsyncInferenceClient:
        return self.__CLIENT

    def get_model(self) -> str:
        return self.__MODEL

    def __repr__(self) -> str:
        """
        String that get's printed when user calls print().
        """
        return "Not allowed to print config."


config = Config()
