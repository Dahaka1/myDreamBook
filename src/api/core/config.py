from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	# sensitive
	OPENAI_API_KEY: str

	# config
	WEB_REQUESTS_DEFAULT_RETRIES_AMOUNT: int = 3


@lru_cache
def get_settings():
	return Settings(_env_file=".env")
