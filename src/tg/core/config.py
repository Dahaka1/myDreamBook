from datetime import timedelta
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	# sensitive
	TELEGRAM_BOT_API_KEY: str
	TELEGRAM_BOT_ID: int
	TELEGRAM_API_BASE_URL: str = "https://api.telegram.org"
	API_HOST: str
	API_PORT: int

	# config
	BOT_UPDATING_PERIOD: timedelta = timedelta(seconds=0.5)
	BOT_UPDATING_LONG_POLLING_TIMEOUT: timedelta = timedelta(seconds=90)
	BOT_UPDATING_ITEMS_LIMIT: int = 100

	# api
	GPT_RESPONSE_TIMEOUT: timedelta = timedelta(seconds=40)


@lru_cache
def get_settings():
	return Settings(_env_file='.env')
