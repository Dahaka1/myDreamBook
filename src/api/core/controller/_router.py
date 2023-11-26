from fastapi import APIRouter, Depends

from models import DreamIn
from services import get_gpt_service, GPTService

router = APIRouter(prefix="/dream")


@router.post("/")
async def get_dream_interpretation(
	dream_info: DreamIn,
	gpt_service: GPTService = Depends(get_gpt_service)
):
	return await gpt_service.get_dream_interpretation(dream_info)
