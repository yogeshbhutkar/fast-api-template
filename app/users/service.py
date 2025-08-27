import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AuthService, CurrentUser
from app.core.exceptions import (
	InvalidPasswordError,
	PasswordMismatchError,
	UserNotFoundError,
)
from app.entities import User
from app.users import models


class UserService:
	"""Service class for managing user operations."""

	def __init__(self, db: AsyncSession, current_user: CurrentUser):
		"""Initialize the UserService with a database session.

		Args:
			db (AsyncSession): The database session.
			current_user (TokenData): The current authenticated user.
		"""
		self.db = db

		user_id = current_user.get_uuid()
		if not user_id:
			logging.error("Invalid user ID in token data.")
			raise UserNotFoundError()
		self.user_id = user_id

	async def get_user_by_id(self) -> User:
		"""Fetch a user by their ID."""
		user = (
			await self.db.execute(select(User).where(User.id == self.user_id))
		).scalar_one_or_none()

		if not user:
			logging.warning(f"User with id {self.user_id} not found.")
			raise UserNotFoundError(self.user_id)

		return user

	async def change_password(
		self,
		password_change: models.PasswordChangeRequest,
	) -> None:
		"""Change the password for a user after verifying the current password."""
		try:
			user = await self.get_user_by_id()

			# Verify current password.
			if not AuthService.verify_password(
				password_change.current_password,
				user.password_hash,
			):
				logging.warning(
					f"Operation failed for {self.user_id}: incorrect current password.",
				)
				raise InvalidPasswordError()

			# Verify new password match.
			if password_change.new_password != password_change.new_password_confirm:
				logging.warning(
					f"Password mismatch for user: {self.user_id}",
				)
				raise PasswordMismatchError()

			# Update password.
			user.password_hash = AuthService.get_password_hash(
				password_change.new_password,
			)
			await self.db.commit()
			logging.info(f"Successfully changed password for user ID: {self.user_id}")

		except Exception as e:
			logging.error(
				f"Error during password change for user {self.user_id}: {str(e)}",
			)
			raise
