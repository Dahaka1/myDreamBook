import asyncio
from typing import Type

import httpx
from httpx import AsyncClient
from yarl import URL

from config import get_settings
from ._abc import UpdatesHandlerProto
from models import TGBotUpdate, DreamInfo, MessageOut
from utils import status_code

settings = get_settings()


class UpdatesHandler(UpdatesHandlerProto):
	_HANDLER_API_HOST = settings.API_HOST
	_HANDLER_API_PORT = settings.API_PORT

	def __init__(
		self,
		http_client: Type[AsyncClient]
	):
		self._http_client = http_client
		self._base_url = self._get_base_url()

	async def handle(self, updates: list[TGBotUpdate]) -> list[MessageOut]:
		messages_out = []
		tasks = []
		if not updates:
			return messages_out

		async def task(update):
			message_chat_id = update.message.chat.id
			message_text = update.message.text

			async with self._http_client() as client:
				dream_data = {"content": message_text}
				dream_info_response = await client.post(
					str(self._base_url / "dream/"),
					json=dream_data,
					timeout=settings.GPT_RESPONSE_TIMEOUT.seconds
				)
			if dream_info_response.status_code == status_code.OK:
				dream_info = DreamInfo(**dream_info_response.json())
				messages_out.append(
					MessageOut(
						chat_id=message_chat_id, text=dream_info.interpretation
					)
				)

		for update in updates:
			tasks.append(task(update))

		try:
			await asyncio.gather(*tasks)
		except httpx.ReadTimeout:
			pass

		return messages_out

	def _get_base_url(self) -> URL:
		return URL(f"http://{self._HANDLER_API_HOST}:{self._HANDLER_API_PORT}")
