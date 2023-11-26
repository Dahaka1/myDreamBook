import asyncio
from typing import Type, Iterable, Any

import httpx
from httpx import AsyncClient
from yarl import URL
from requests import get as http_get

from config import get_settings
from utils.logging import get_logger
from ._abc import _BotBase
from models import TGBotUpdate, MessageOut, BotUpdateStorageModel
from service import UpdatesHandlerProto
from utils.exceptions import TGBotException
from utils import status_code

settings = get_settings()

logger = get_logger()

_not_implemented_url_exc = TGBotException("Bot base url isn't implemented")


class Bot(_BotBase):
	_BASE_URL: str = None
	_UPDATING_TIMEOUT = settings.BOT_UPDATING_LONG_POLLING_TIMEOUT.seconds

	def __init__(
		self,
		api_key: str,
		base_url: str,
		http_client: Type[AsyncClient],
		updates_handler: Any
	):
		self._api_key = api_key
		self._updates: list[TGBotUpdate] = []
		self._available = False
		self._http_client = http_client
		self._connected = False
		self._updates_handler: UpdatesHandlerProto = updates_handler
		self._updates_offset: int | None = None

		self.__class__._BASE_URL = self._get_base_url(base_url)
		self._get_state()

	async def start(self) -> None:
		if not self._BASE_URL:
			raise _not_implemented_url_exc
		if not self._available:
			raise TGBotException("Cannot establish the connection to Telegram API server")
		logger.info("Bot starting up")
		await self._run_loop()

	def stop(self) -> None:
		logger.info("Bot shutting down")

	async def _run_loop(self) -> None:
		while True:
			if not self._connected:
				await self._update()
				messages_out = await self._updates_handler.handle(self._updates)
				await self._send_messages(messages_out)
				self._updates.clear()
				self._updates_offset += 1
			await asyncio.sleep(settings.BOT_UPDATING_PERIOD.seconds)

	async def _update(self) -> None:
		updates = []
		async with self._http_client() as client:
			self._connected = True
			try:
				logger.info("Waiting for updates...")
				updates_response = await client.get(
					str(self._BASE_URL / "getUpdates"),
					params=self._get_timeout_params(self._updates_offset),
					timeout=self._UPDATING_TIMEOUT
				)
				if updates_response.status_code == status_code.OK:
					updates = [TGBotUpdate(**upd) for upd in updates_response.json()["result"]]
			except (TimeoutError, httpx.ReadTimeout):
				pass
			finally:
				await updates_response.aclose()
				self._connected = False
		if updates:
			self._updates.extend(updates)
			self._updates_offset = updates[-1].id
			logger.info(f"There are {len(updates)} bot updates was received")

	def _get_timeout_params(self, offset: int | None) -> dict:
		params = {
			"timeout": self._UPDATING_TIMEOUT,
			"limit": settings.BOT_UPDATING_ITEMS_LIMIT,
			"allowed_updates": ["message"],
		}
		if offset:
			params["offset"] = offset
		return params

	def _get_state(self) -> None:
		if not self._BASE_URL:
			raise _not_implemented_url_exc
		state_response = http_get(self._BASE_URL / "getMe")
		if state_response.status_code == status_code.OK:
			bot_id = state_response.json().get("result", {}).get("id", None)
			if bot_id == settings.TELEGRAM_BOT_ID:
				self._available = True
		return None

	def _get_base_url(self, url: str) -> URL:
		return URL(url) / self._api_key

	async def _send_messages(self, messages: list[MessageOut]) -> None:
		if not messages:
			return
		tasks = []
		sended_messages = set()

		async def task(message: MessageOut):
			with self._http_client() as client:
				message_sending_result = await client.post(
					str(self._BASE_URL / "sendMessage"),
					json=message.model_dump(mode="json")
				)
				if message_sending_result.status_code == status_code.OK:
					sended_messages.add(
						message_sending_result.json()["message_id"]
					)

		for msg in messages:
			tasks.append(task(msg))

		await asyncio.gather(*tasks)

		logger.info(f"There are {len(sended_messages)} was sended")
