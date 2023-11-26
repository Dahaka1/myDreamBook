from pydantic import BaseModel, Field

from ._abc import JSONModel


class _DreamBase(JSONModel):
	content: str = Field(max_length=300)


class DreamIn(_DreamBase):
	pass


class Dream(DreamIn):
	interpretation: str | None
