import pydantic

class LangFuseResponse(pydantic.BaseModel):
	message: str

class LangFuseRequest(pydantic.BaseModel):
	question: str = "What is your name?"