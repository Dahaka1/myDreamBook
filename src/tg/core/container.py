from httpx import AsyncClient

from controller import Bot
from service._handler import UpdatesHandler
from config import get_settings

settings = get_settings()

__bot_updates_handler = UpdatesHandler(
	http_client=AsyncClient
)

bot = Bot(
	api_key=settings.TELEGRAM_BOT_API_KEY,
	base_url=settings.TELEGRAM_API_BASE_URL,
	http_client=AsyncClient,
	updates_handler=__bot_updates_handler
)
