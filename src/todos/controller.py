from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.todos import models
from src.todos.dependencies import get_todo_service
from src.todos.service import TodoService

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
	todo: models.TodoCreate,
	todo_service: TodoService = Depends(get_todo_service),
):
	return await todo_service.create_todo(todo)


@router.get("/", response_model=list[models.TodoResponse])
async def get_todos(todo_service: TodoService = Depends(get_todo_service)):
	return await todo_service.get_todos()


@router.get("/{todo_id}", response_model=models.TodoResponse)
async def get_todo(
	todo_id: UUID,
	todo_service: TodoService = Depends(get_todo_service),
):
	return await todo_service.get_todo_by_id(todo_id)


@router.put("/{todo_id}", response_model=models.TodoResponse)
async def update_todo(
	todo_id: UUID,
	todo_update: models.TodoCreate,
	todo_service: TodoService = Depends(get_todo_service),
):
	return await todo_service.update_todo(todo_id, todo_update)


@router.put("/{todo_id}/complete", response_model=models.TodoResponse)
async def complete_todo(
	todo_id: UUID,
	todo_service: TodoService = Depends(get_todo_service),
):
	return await todo_service.complete_todo(todo_id)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
	todo_id: UUID,
	todo_service: TodoService = Depends(get_todo_service),
):
	await todo_service.delete_todo(todo_id)
	return {"message": "Todo deleted successfully"}
