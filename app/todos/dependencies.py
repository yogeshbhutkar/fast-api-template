from app.auth.service import CurrentUser
from app.database.core import DBSession
from app.todos.service import TodoService


def get_todo_service(
	db: DBSession,
	current_user: CurrentUser,
) -> TodoService:
	return TodoService(db, current_user)
