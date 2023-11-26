from pydantic import BaseModel


class DreamInfo(BaseModel):
	content: str
	interpretation: str
