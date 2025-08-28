import fastapi

from src.langfuse.dependency import get_langfuse_service
from src.langfuse.model import LangFuseRequest, LangFuseResponse
from src.langfuse.service import LangFuseLoggingService

router = fastapi.APIRouter(
	prefix="/langfuse",
	tags=["langfuse"],
)

@router.post(
    "/",
    response_model=LangFuseResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def create_langfuse_item(
    request: LangFuseRequest,
    langfuse_service: LangFuseLoggingService = fastapi.Depends(get_langfuse_service),
):
    return await langfuse_service.log_event(request)
