from app.auth.service import CurrentUser
from app.database.core import DBSession
from app.users.service import UserService


def get_user_service(db: DBSession, current_user: CurrentUser) -> UserService:
	return UserService(db, current_user)
