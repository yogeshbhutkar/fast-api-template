from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class UserResponse(BaseModel):
	id: UUID
	email: EmailStr
	first_name: str
	last_name: str

class PasswordChangeRequest(BaseModel):
	current_password: str = Field(..., min_length=8, max_length=128)
	new_password: str =Field(..., min_length=8, max_length=128)
	new_password_confirm: str = Field(..., min_length=8, max_length=128)
