import uuid
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..database.core import Base

class User(Base):
	__tablename__ = "users"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
	first_name: Mapped[str] = mapped_column(String, nullable=False)
	last_name: Mapped[str] = mapped_column(String, nullable=False)
	password_hash: Mapped[str] = mapped_column(String, nullable=False)

	def __repr__(self):
		return f"<User(email='{self.email}', first_name='{self.first_name}', last_name='{self.last_name}')>"
