from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.entities import Priority


class TodoBase(BaseModel):
	description: str
	due_date: datetime | None = None
	priority: Priority = Priority.Medium


class TodoCreate(TodoBase):
	pass


class TodoResponse(TodoBase):
	id: UUID
	is_completed: bool
	completed_at: datetime | None = None

	model_config = ConfigDict(from_attributes=True)
