import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv(override=True)


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

    def get_hf_token(self):
        return self.__HF_TOKEN

    def get_model(self):
        return self.__MODEL

    def __repr__(self) -> str:
        """
        String that get's printed when user calls print().
        """
        return "Not allowed to print config."


config = Config()
