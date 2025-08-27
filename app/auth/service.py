import logging
from datetime import UTC, datetime, timedelta
from typing import Annotated, cast
from uuid import UUID, uuid4

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from jwt import decode as jwt_decode
from jwt import encode as jwt_encode
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import models
from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.entities import User

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
	"""Service class for managing authentication operations."""

	def __init__(self, db: AsyncSession):
		"""Initialize the AuthService with a database session.
		Args:
			db (AsyncSession): The database session.
		"""
		self.db = db

	@staticmethod
	def verify_password(plain_password: str, hashed_password: str) -> bool:
		"""Verify a plain password against its hashed version."""
		return bcrypt_context.verify(plain_password, hashed_password)

	@staticmethod
	def get_password_hash(password: str) -> str:
		"""Hash a plain password."""
		return bcrypt_context.hash(password)

	@staticmethod
	def verify_token(token: str) -> models.TokenData:
		"""Verify and decode a JWT token to extract user information."""
		try:
			payload = jwt_decode(
				token,
				settings.AUTH_SECRET_KEY,
				algorithms=[settings.AUTH_ALGORITHM],
			)

			user_id: str = str(payload.get("id"))
			return models.TokenData(user_id=user_id)
		except PyJWTError as e:
			logging.error(f"Token verification failed: {str(e)}")
			raise AuthenticationError("Could not validate credentials")

	async def _authenticate_user(
		self,
		email: str,
		password: str,
	) -> User | None:
		"""Authenticate a user by their email and password."""
		user = (
			await self.db.execute(select(User).where(User.email == email))
		).scalar_one_or_none()

		if not user or not self.verify_password(password, user.password_hash):
			return None

		return user

	def _create_access_token(
		self,
		email: str,
		user_id: UUID,
		expires_delta: timedelta,
	) -> str:
		"""Create a JWT access token for a user."""
		encode: dict[str, str | datetime] = {
			"sub": email,
			"id": str(user_id),
			"exp": datetime.now(UTC) + expires_delta,
		}

		token = jwt_encode(
			encode,
			settings.AUTH_SECRET_KEY,
			algorithm=settings.AUTH_ALGORITHM,
		)

		return cast("str", token)

	async def register_user(
		self,
		register_user_request: models.RegisterUserRequest,
	) -> None:
		"""Register a new user in the system."""
		try:
			create_user_model = User(
				id=uuid4(),
				email=register_user_request.email,
				first_name=register_user_request.first_name,
				last_name=register_user_request.last_name,
				password_hash=self.get_password_hash(register_user_request.password),
			)

			self.db.add(create_user_model)
			await self.db.commit()
		except Exception as e:
			logging.error(
				f"Registration failed: {register_user_request.email}. Error: {str(e)}",
			)
			raise AuthenticationError("Error registering user")

	async def login_for_access_token(
		self,
		form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
	) -> models.Token:
		"""Authenticate user and provide an access token."""
		user = await self._authenticate_user(
			form_data.username,
			form_data.password,
		)

		if user is None:
			raise AuthenticationError()

		token = self._create_access_token(
			user.email,
			user.id,
			timedelta(minutes=settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES),
		)

		return models.Token(access_token=token, token_type="bearer")


def get_current_user(
	token: Annotated[str, Depends(oauth2_bearer)],
) -> models.TokenData:
	"""Dependency to get the current authenticated user from the token."""
	return AuthService.verify_token(token)


CurrentUser = Annotated[models.TokenData, Depends(get_current_user)]
