import asyncio
import sys

from config import get_settings
from container import bot

settings = get_settings()


async def main():
	await bot.start()


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(main())
	except KeyboardInterrupt:
		bot.stop()
		sys.exit(0)
