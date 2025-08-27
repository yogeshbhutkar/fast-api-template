from src.auth.service import CurrentUser
from src.database.core import DBSession
from src.todos.service import TodoService


def get_todo_service(
	db: DBSession,
	current_user: CurrentUser,
) -> TodoService:
	return TodoService(db, current_user)
