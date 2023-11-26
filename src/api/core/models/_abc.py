from typing import Any

from pydantic import BaseModel
import orjson


class JSONModel(BaseModel):
	def jsonable_dict(self, *args, **kwargs) -> Any:
		model_dict: dict = self.model_dump(*args, **kwargs)
		return orjson.loads(orjson.dumps(model_dict).decode())
