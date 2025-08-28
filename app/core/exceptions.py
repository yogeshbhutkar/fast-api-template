from uuid import UUID

from fastapi import HTTPException, status


class AuthenticationError(HTTPException):
	def __init__(self, message: str = "Could not validate credentials"):
		super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


class UserNotFoundError(HTTPException):
	def __init__(self, user_id: UUID | None = None):
		message = (
			"User not found" if user_id is None else f"User with id {user_id} not found"
		)
		super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class InvalidPasswordError(HTTPException):
	def __init__(self):
		super().__init__(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Current password is incorrect",
		)


class PasswordMismatchError(HTTPException):
	def __init__(self):
		super().__init__(status_code=400, detail="New passwords do not match")


class TodoCreationError(HTTPException):
	def __init__(self, error: str):
		super().__init__(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"Failed to create todo: {error}",
		)
