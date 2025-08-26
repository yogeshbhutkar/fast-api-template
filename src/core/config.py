from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
	API_PREFIX: str = "/api"
	DEBUG: bool = False
	DATABASE_URL: str = ""
	SQLALCHEMY_ECHO: bool = False
	ALLOWED_ORIGINS: str = ""
	OPENAI_API_KEY: str = ""
	AUTH_SECRET_KEY: str = ""
	AUTH_ALGORITHM: str = "HS256"
	AUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

	@field_validator("ALLOWED_ORIGINS")
	def parse_allowed_origins(cls, v: str) -> List[str]:
		return v.split(",") if v else []

	class Config:
		env_file = ".env"
		env_file_encoding = "utf-8"
		case_sensitive = True

settings = Settings()
