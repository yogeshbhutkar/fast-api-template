from src.auth.service import CurrentUser
from src.database.core import DBSession
from src.users.service import UserService


def get_user_service(db: DBSession, current_user: CurrentUser) -> UserService:
	return UserService(db, current_user)
