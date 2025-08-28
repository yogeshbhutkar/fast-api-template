from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	"""
	Application settings.

	Loads settings from environment variables or a .env file.
	"""

	API_PREFIX: str = "/api"
	DEBUG: bool = False
	DATABASE_URL: str = ""
	ALEMBIC_DATABASE_URL: str = ""
	SQLALCHEMY_ECHO: bool = False
	ALLOWED_ORIGINS: str = ""
	OPENAI_API_KEY: str = ""
	AUTH_SECRET_KEY: str = ""
	AUTH_ALGORITHM: str = "HS256"
	AUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

	@classmethod
	@field_validator("ALLOWED_ORIGINS")
	def parse_allowed_origins(cls, v: str) -> list[str]:
		return v.split(",") if v else []

	class Config:
		env_file = ".env"
		env_file_encoding = "utf-8"
		case_sensitive = True

load_dotenv()
settings = Settings()
