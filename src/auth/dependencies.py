from src.auth.service import AuthService
from src.database.core import DBSession


def get_auth_service(db: DBSession) -> AuthService:
	return AuthService(db)
