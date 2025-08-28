import logging
from datetime import UTC, datetime
from typing import cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import TokenData
from app.core.exceptions import TodoCreationError, UserNotFoundError
from app.entities import Todo
from app.todos import models


class TodoService:
	"""Service class for managing todo operations.

	Attributes:
		db (AsyncSession): The database session for performing CRUD operations.
		current_user (TokenData): The current authenticated user.
	"""

	def __init__(self, db: AsyncSession, current_user: TokenData):
		"""Initialize the TodoService with a database session and current user.

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

	async def create_todo(
		self,
		todo: models.TodoCreate,
	) -> Todo:
		"""Create a new todo item."""
		try:
			new_todo = Todo(**todo.model_dump())
			new_todo.user_id = self.user_id

			self.db.add(new_todo)
			await self.db.commit()
			await self.db.refresh(new_todo)

			return new_todo
		except Exception as e:
			logging.error(
				f"Error creating todo for user {self.user_id}: {str(e)}",
			)
			raise TodoCreationError(error=str(e))

	async def get_todos(self) -> list[Todo]:
		"""Retrieve all todo items."""
		return cast(
			"list[Todo]",
			(await self.db.execute(select(Todo).where(Todo.user_id == self.user_id)))
			.scalars()
			.all(),
		)

	async def get_todo_by_id(
		self,
		todo_id: UUID,
	) -> Todo:
		"""Retrieve a specific todo item by its ID."""
		todo = (
			await self.db.execute(
				select(Todo).where(Todo.id == todo_id, Todo.user_id == self.user_id),
			)
		).scalar_one_or_none()

		if not todo:
			logging.warning(f"Todo with id {todo_id} not found USER:{self.user_id}.")
			raise UserNotFoundError(self.user_id)

		return todo

	async def update_todo(
		self,
		todo_id: UUID,
		todo_update: models.TodoCreate,
	) -> Todo:
		"""Update an existing todo item for the current user."""
		todo = await self.get_todo_by_id(todo_id)
		todo_data = todo_update.model_dump(exclude_unset=True)

		for key, value in todo_data.items():
			if hasattr(todo, key):
				setattr(todo, key, value)

		await self.db.commit()
		await self.db.refresh(todo)
		return todo

	async def complete_todo(
		self,
		todo_id: UUID,
	) -> Todo:
		"""Mark a specific todo item as completed."""
		todo = await self.get_todo_by_id(todo_id)
		if todo.is_completed:
			return todo

		todo.is_completed = True
		todo.completed_at = datetime.now(UTC)

		await self.db.commit()
		await self.db.refresh(todo)
		return todo

	async def delete_todo(
		self,
		todo_id: UUID,
	) -> None:
		"""Delete a specific todo item by its ID."""
		todo = await self.get_todo_by_id(todo_id)
		await self.db.delete(todo)
		await self.db.commit()
