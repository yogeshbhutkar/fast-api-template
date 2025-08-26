from fastapi import APIRouter, status

from src.auth.service import CurrentUser
from src.database.core import DBSession
from src.users import models, service

router = APIRouter(
	prefix="/users",
	tags=["users"],
)

@router.get("/me", response_model=models.UserResponse)
async def get_current_user(current_user: CurrentUser, db: DBSession):
	return await service.get_user_by_id(db, current_user.get_uuid())

@router.put("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
	password_change: models.PasswordChangeRequest,
	db: DBSession,
	current_user: CurrentUser
):
	await service.change_password(db, current_user.get_uuid(), password_change)
	return {"message": "Password changed successfully"}