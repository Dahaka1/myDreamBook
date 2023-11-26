from typing import Callable, Type

from config import get_settings

settings = get_settings()


def retry_on_exc(
	retry_on_errors: list[Type[Exception]],
	retries_amount=settings.WEB_REQUESTS_DEFAULT_RETRIES_AMOUNT
):
	def sub_wrapper(foo: Callable):
		async def wrapper(*args, **kwargs):
			result = None
			for _ in range(retries_amount):
				try:
					result = await foo(*args, **kwargs)
				except retry_on_errors:
					pass
			return result
		return wrapper
	return sub_wrapper
