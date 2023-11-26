from fastapi import FastAPI

from config import get_settings
from controller import router
from utils.logging import get_logger

settings = get_settings()
logger = get_logger()

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
def starting_up():
	logger.info("Starting server")
