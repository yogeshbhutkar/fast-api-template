from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth import models
from src.auth.dependencies import get_auth_service
from src.auth.service import AuthService
from src.core.rate_limiting import rate_limit

router = APIRouter(
	prefix="/auth",
	tags=["auth"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
@rate_limit("5/hour")
async def register_user(
	request: Request,
	register_user_request: models.RegisterUserRequest,
	auth_service: AuthService = Depends(get_auth_service),
):
	"""
	Register a new user.
	"""
	await auth_service.register_user(register_user_request)
	return {"message": "User registered successfully."}


@router.post("/token", response_model=models.Token)
async def login_for_access_token(
	form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
	auth_service: AuthService = Depends(get_auth_service),
):
	"""
	Authenticate user and provide an access token.
	"""
	return await auth_service.login_for_access_token(form_data)
