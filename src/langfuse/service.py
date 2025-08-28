from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from langfuse import get_client, observe
from src.core.config import settings
from src.langfuse.model import LangFuseRequest, LangFuseResponse


class LangFuseLoggingService:
	def __init__(self):
		self.llm = ChatGoogleGenerativeAI(
			model="gemini-1.5-flash",
			google_api_key=settings.GOOGLE_API_KEY,
			temperature=0.7,
		)

	@observe
	async def log_event(self, request: LangFuseRequest) -> LangFuseResponse:
		message = HumanMessage(content=request.question)

		try:
			# The @observe decorator will automatically track this LLM call
			response = await self.llm.ainvoke([message])

			response_text = (
				str(response.content) if response.content else "No response received"
			)

			return LangFuseResponse(message=response_text)

		except Exception as e:
			# The @observe decorator will automatically capture exceptions
			return LangFuseResponse(message=f"Error processing request: {str(e)}")
		finally:
			# Ensure all events are flushed to Langfuse
			langfuse = get_client()
			langfuse.flush()
