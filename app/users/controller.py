from fastapi import APIRouter, Depends, status

from app.users import models
from app.users.dependencies import get_user_service
from app.users.service import UserService

router = APIRouter(
	prefix="/users",
	tags=["users"],
)


@router.get("/me", response_model=models.UserResponse)
async def get_current_user(
	user_service: UserService = Depends(get_user_service),
):
	return await user_service.get_user_by_id()


@router.put("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
	password_change: models.PasswordChangeRequest,
	user_service: UserService = Depends(get_user_service),
):
	await user_service.change_password(password_change)
	return {"message": "Password changed successfully"}
