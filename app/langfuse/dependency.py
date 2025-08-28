from app.langfuse.service import LangFuseLoggingService


def get_langfuse_service() -> LangFuseLoggingService:
	return LangFuseLoggingService()
