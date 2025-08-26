import enum
import uuid
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

from ..database.core import Base

class Priority(enum.Enum):
	Normal = 0
	Low = 1
	Medium = 2
	High = 3
	Top = 4

class Todo(Base):
	__tablename__ = "todos"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
	description: Mapped[str] = mapped_column(String, nullable=False)
	due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
	is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
	completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
	priority: Mapped[Priority]= mapped_column(Enum(Priority), nullable=False, default=Priority.Medium)

	def __repr__(self):
		return f"<Todo(description='{self.description}', due_date='{self.due_date}', is_completed={self.is_completed}, priority={self.priority})>"