import logging
from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import get_password_hash, verify_password
from src.core.exceptions import InvalidPasswordError, PasswordMismatchError, UserNotFoundError
from src.entities.user import User
from src.users import models

async def get_user_by_id(db: AsyncSession, user_id: Optional[UUID]) -> User:
	if not user_id:
		raise UserNotFoundError()

	user = (await db.execute(
		select(User).where(User.id == user_id)
	)).scalar_one_or_none()

	if not user:
		logging.warning(f"User with id {user_id} not found.")
		raise UserNotFoundError(user_id)

	return user

async def change_password(
	db: AsyncSession,
	user_id: Optional[UUID],
	password_change: models.PasswordChangeRequest,
) -> None:
	if not user_id:
		raise UserNotFoundError()

	try:
		user = await get_user_by_id(db, user_id)

		# Verify current password.
		if not verify_password(password_change.current_password, user.password_hash):
			logging.warning(f"Password change failed for user id {user_id}: incorrect current password.")
			raise InvalidPasswordError()
		
		# Verify new password match.
		if password_change.new_password != password_change.new_password_confirm:
			logging.warning(f"Password mismatch during change attempt for user ID: {user_id}")
			raise PasswordMismatchError()
		
		# Update password.
		user.password_hash = get_password_hash(password_change.new_password)
		await db.commit()
		logging.info(f"Successfully changed password for user ID: {user_id}")

	except Exception as e:
		logging.error(f"Error during password change for user id {user_id}: {str(e)}")
		raise
