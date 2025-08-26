from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class RegisterUserRequest(BaseModel):
	email: EmailStr
	first_name: str = Field(..., min_length=1, max_length=50)
	last_name: str = Field(..., min_length=1, max_length=50)
	password: str = Field(..., min_length=8, max_length=128)

class Token(BaseModel):
	access_token: str
	token_type: str
	
class TokenData(BaseModel):
	user_id: str | None = None

	def get_uuid(self) -> UUID | None:
		if self.user_id:
			return UUID(self.user_id)
		return None