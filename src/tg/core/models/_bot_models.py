from pydantic import BaseModel, Field


class User(BaseModel):
	id: int
	first_name: str
	last_name: str | None = None
	username: str | None


class Chat(BaseModel):
	id: int


class Message(BaseModel):
	id: int = Field(alias="message_id")
	from_: User | None = Field(alias="from")
	chat: Chat
	text: str | None
	date: int


class MessageOut(BaseModel):
	chat_id: int | str
	text: str = Field(min_length=1, max_length=4096)


class TGBotUpdate(BaseModel):
	id: int = Field(alias="update_id")
	message: Message
