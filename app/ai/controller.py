from fastapi import APIRouter

from app.ai import models
from app.ai.service import generate_response

router = APIRouter(
	prefix="/ai-engine",
	tags=["ai-engine"],
)


@router.post("/summarize")
def summarize_text():
	return {"message": "Text summarized successfully"}


@router.post("/generate")
async def generate_content(user_query: models.UserQuery):
	return generate_response(user_query.user_query)
