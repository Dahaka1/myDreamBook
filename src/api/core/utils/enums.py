from enum import Enum


class GPTModelEnum(Enum):
	GPT_35_TURBO = "gpt-3.5-turbo"


class GPTRoleEnum(Enum):
	SYSTEM = "system"
	USER = "user"
	ASSISTANT = "assistant"


class GPTFinishReasonEnum(Enum):
	STOP = "stop"
	LENGTH = "length"
	FUNCTION_CALL = "function_call"
	CONTENT_FILTER = "content_filter"
