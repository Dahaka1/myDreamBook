from typing import ClassVar, Protocol, Any


class UpdatesHandlerProto(Protocol):
	_HANDLER_API_HOST: ClassVar[str]
	_HANDLER_API_PORT: ClassVar[int]

	async def handle(self, updates: Any):
		raise NotImplementedError
