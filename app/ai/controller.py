import inngest
from fastapi import APIRouter

from app.ai import models
from app.core.adapters.inngest import inngest_client

router = APIRouter(
	prefix="/ai-engine",
	tags=["ai-engine"],
)


@router.post("/summarize")
def summarize_text():
	return {"message": "Text summarized successfully"}


@router.post("/generate")
async def generate_content(user_query: models.UserQuery):
	return await inngest_client.send(
		inngest.Event(
			name="say-hello",
			data={
				"query": user_query.user_query,
			},
		),
	)
