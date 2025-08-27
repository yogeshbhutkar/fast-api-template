from uuid import UUID

from fastapi import APIRouter, status

from src.auth.service import CurrentUser
from src.database.core import DBSession
from src.todos import models, service

router = APIRouter(
	prefix="/todos",
	tags=["todos"],
)


@router.post(
	"/",
	response_model=models.TodoResponse,
	status_code=status.HTTP_201_CREATED,
)
async def create_todo(
	db: DBSession,
	todo: models.TodoCreate,
	current_user: CurrentUser,
):
	return await service.create_todo(current_user, db, todo)


@router.get("/", response_model=list[models.TodoResponse])
async def get_todos(db: DBSession, current_user: CurrentUser):
	return await service.get_todos(current_user, db)


@router.get("/{todo_id}", response_model=models.TodoResponse)
async def get_todo(db: DBSession, todo_id: UUID, current_user: CurrentUser):
	return await service.get_todo_by_id(current_user, db, todo_id)


@router.put("/{todo_id}", response_model=models.TodoResponse)
async def update_todo(
	db: DBSession,
	todo_id: UUID,
	todo_update: models.TodoCreate,
	current_user: CurrentUser,
):
	return await service.update_todo(current_user, db, todo_id, todo_update)


@router.put("/{todo_id}/complete", response_model=models.TodoResponse)
async def complete_todo(db: DBSession, todo_id: UUID, current_user: CurrentUser):
	return await service.complete_todo(current_user, db, todo_id)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: DBSession, todo_id: UUID, current_user: CurrentUser):
	await service.delete_todo(current_user, db, todo_id)
	return {"message": "Todo deleted successfully"}
