from dataclasses import dataclass

from models import TGBotUpdate


@dataclass
class _BotUpdateModelInfo:
	user_id: int | None
	username: str | None
	text: str | None


@dataclass
class BotUpdateStorageModel:
	user_info: _BotUpdateModelInfo
	handled: bool = False

	@classmethod
	def from_tg_update(cls, tg_update: TGBotUpdate) -> "BotUpdateStorageModel":
		if tg_update.message:
			user_info = _BotUpdateModelInfo(
				user_id=tg_update.message.from_.id,
				username=tg_update.message.from_.username,
				text=tg_update.message.text
			)
		else:
			user_info = _BotUpdateModelInfo(None, None, None)
		return cls(
			user_info=user_info
		)
