from fastapi import APIRouter, status, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from ..core.rate_limiting import rate_limit
from ..database.core import DBSession
from ..auth import service, models

router = APIRouter(
	prefix="/auth",
	tags=["auth"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
@rate_limit("5/hour")
async def register_user(request: Request, db: DBSession, register_user_request: models.RegisterUserRequest):
	"""
	Register a new user.
	"""
	await service.register_user(db, register_user_request)
	return {"message": "User registered successfully."}

@router.post("/token", response_model=models.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DBSession):
	"""
	Authenticate user and provide an access token.
	"""
	return await service.login_for_access_token(form_data, db)