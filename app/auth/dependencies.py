from app.auth.service import AuthService
from app.database.core import DBSession


def get_auth_service(db: DBSession) -> AuthService:
	return AuthService(db)
