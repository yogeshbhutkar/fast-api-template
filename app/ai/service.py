import inngest
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

from app.core.adapters.inngest import inngest_client

try:
	load_dotenv()
	model = init_chat_model(
		model="gemini-2.5-flash",
		model_provider="google_genai",
	)
except Exception as e:
	print("Error initializing the model:", e)
	raise e


@inngest_client.create_function(
	fn_id="hello-world",
	trigger=inngest.TriggerEvent(event="say-hello"),
)
async def generate_response(ctx: inngest.Context) -> str:
	"""Generate a response from the LLM based on the user query."""
	messages: list[SystemMessage | HumanMessage] = [
		SystemMessage(content="Translate the following from English into Italian"),
		HumanMessage(content=ctx.event.data["query"]),  # type: ignore
	]

	response = model.invoke(messages)
	return response.content  # type: ignore
