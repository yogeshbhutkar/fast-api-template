import logging
from typing import List, cast
from uuid import UUID
from src.auth.models import TokenData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from ..core.exceptions import TodoCreationError, UserNotFoundError
from ..entities import Todo
from ..todos import models

async def create_todo(
	current_user: TokenData,
	db: AsyncSession,
	todo: models.TodoCreate
) -> Todo:
	try:
		new_todo = Todo(**todo.model_dump())
		user_id = current_user.get_uuid()

		if not user_id:
			raise UserNotFoundError()
		
		new_todo.user_id = user_id
		
		db.add(new_todo)
		await db.commit()
		await db.refresh(new_todo)
		
		return new_todo
	except Exception as e:
		logging.error(f"Error creating todo for user {current_user.user_id}: {str(e)}")
		raise TodoCreationError(error=str(e))

async def get_todos(current_user: TokenData, db: AsyncSession) -> List[Todo]:
	user_id = current_user.get_uuid()
	if not user_id:
		raise UserNotFoundError()

	todos = cast(List[Todo], (
		await db.execute(
			select(Todo).where(Todo.user_id == user_id))
		).scalars().all()
	)

	return todos

async def get_todo_by_id(
	current_user: TokenData,
	db: AsyncSession,
	todo_id: UUID
) -> Todo:
	user_id = current_user.get_uuid()
	if not user_id:
		raise UserNotFoundError()

	todo = (await db.execute(
		select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
	)).scalar_one_or_none()

	if not todo:
		logging.warning(f"Todo with id {todo_id} not found for user {user_id}.")
		raise UserNotFoundError(user_id)

	return todo

async def update_todo(
	current_user: TokenData,
	db: AsyncSession,
	todo_id: UUID,
	todo_update: models.TodoCreate
) -> Todo:
	todo = await get_todo_by_id(current_user, db, todo_id)
	todo_data = todo_update.model_dump(exclude_unset=True)

	for key, value in todo_data.items():
		if hasattr(todo, key):
			setattr(todo, key, value)

	await db.commit()
	await db.refresh(todo)
	return todo

async def complete_todo(
	current_user: TokenData,
	db: AsyncSession,
	todo_id: UUID
) -> Todo:
	todo = await get_todo_by_id(current_user, db, todo_id)
	if todo.is_completed:
		return todo

	todo.is_completed = True
	todo.completed_at = datetime.now(timezone.utc)

	await db.commit()
	await db.refresh(todo)
	return todo

async def delete_todo(
	current_user: TokenData,
	db: AsyncSession,
	todo_id: UUID
) -> None:
	todo = await get_todo_by_id(current_user, db, todo_id)
	await db.delete(todo)
	await db.commit()
