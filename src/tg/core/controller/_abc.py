import abc
from typing import ClassVar

from yarl import URL


class _BotBase(abc.ABC):
	BASE_URL: ClassVar[URL]

	@abc.abstractmethod
	async def start(self) -> None:
		pass

	@abc.abstractmethod
	def stop(self) -> None:
		pass

	@abc.abstractmethod
	async def _update(self) -> None:
		pass

	@abc.abstractmethod
	def _get_state(self) -> bool:
		pass
