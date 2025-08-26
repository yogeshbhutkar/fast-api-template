import logging
from datetime import timedelta, datetime, timezone
from typing import Annotated, Dict, Union, cast, Optional
from uuid import UUID, uuid4
from fastapi import Depends
from passlib.context import CryptContext
from jwt import PyJWTError, encode as jwt_encode, decode as jwt_decode
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import select

from ..entities.user import User
from ..auth import models
from ..core.config import settings
from ..core.exceptions import AuthenticationError

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
	return bcrypt_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
	return bcrypt_context.hash(password)

async def authenticate_user(
	email: str,
	password: str,
	db: AsyncSession
) -> Optional[User]:
	user = (await db.execute(
		select(User).where(User.email==email))
	).scalar_one_or_none()

	if not user or not verify_password(password, user.password_hash):
		return None

	return user

def create_access_token(
	email: str,
	user_id: UUID,
	expires_delta: timedelta
) -> str:
	encode: Dict[str, Union[str, datetime]] = {
		"sub": email,
		"id": str(user_id),
		"exp": datetime.now(timezone.utc) + expires_delta
	}

	token = jwt_encode(
		encode,
		settings.AUTH_SECRET_KEY,
		algorithm=settings.AUTH_ALGORITHM
	)

	return cast(str, token)

def verify_token(token: str) -> models.TokenData:
	try:
		payload = jwt_decode(
			token,
			settings.AUTH_SECRET_KEY,
			algorithms=[settings.AUTH_ALGORITHM]
		)

		user_id: str = str(payload.get("id"))
		return models.TokenData(user_id=user_id)
	except PyJWTError as e:
		logging.error(f"Token verification failed: {str(e)}")
		raise AuthenticationError("Could not validate credentials")
	
async def register_user(
	db: AsyncSession,
	register_user_request: models.RegisterUserRequest,
) -> None:
	try:
		create_user_model = User(
			id = uuid4(),
			email = register_user_request.email,
			first_name = register_user_request.first_name,
			last_name = register_user_request.last_name,
			password_hash = get_password_hash(register_user_request.password)
		)

		db.add(create_user_model)
		await db.commit()
	except Exception as e:
		logging.error(f"Failed to register user: {register_user_request.email}. Error: {str(e)}")
		raise AuthenticationError("Error registering user")

def get_current_user(
	token: Annotated[str, Depends(oauth2_bearer)]
) -> models.TokenData:
	return verify_token(token)

async def login_for_access_token(
	form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
	db: AsyncSession
) -> models.Token:
	user = await authenticate_user(
		form_data.username,
		form_data.password,
		db,
	)

	if user is None:
		raise AuthenticationError()

	token = create_access_token(
		user.email,
		user.id,
		timedelta(minutes=settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES),
	)

	return models.Token(access_token=token, token_type="bearer")

CurrentUser = Annotated[models.TokenData, Depends(get_current_user)]