from pydantic import Field

from ._abc import JSONModel
from utils.enums import GPTModelEnum, GPTRoleEnum, GPTFinishReasonEnum


class _GPTMessageBase(JSONModel):
	role: GPTRoleEnum = GPTRoleEnum.USER
	content: str


class GPTMessage(_GPTMessageBase):
	@classmethod
	def create_system_message(cls, message: str) -> "GPTMessage":
		return cls(
			role=GPTRoleEnum.SYSTEM,
			content=message
		)


class _GPTQueryBase(JSONModel):
	model: GPTModelEnum = GPTModelEnum.GPT_35_TURBO
	messages: list[GPTMessage] = Field(default_factory=list)


class _GPTChoice(JSONModel):
	finish_reason: GPTFinishReasonEnum | None
	index: int
	message: GPTMessage


class _GPTResponseBase(JSONModel):
	choices: list[_GPTChoice]
	created: int
	id: str
	model: GPTModelEnum

	@property
	def content(self) -> str:
		return self.choices[0].message.content


class GPTQuery(_GPTQueryBase):
	@property
	def content(self) -> str:
		return self.messages[-1].content


class GPTResponse(_GPTResponseBase):
	pass
