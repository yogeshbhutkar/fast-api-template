import datetime
from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import DateTime, MetaData
from sqlalchemy.ext.asyncio import (
	AsyncAttrs,
	AsyncSession,
	async_sessionmaker,
	create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(AsyncAttrs, DeclarativeBase):
	"""Base class for all models."""

	metadata = MetaData(
		naming_convention={
			"ix": "ix_%(column_0_label)s",
			"uq": "uq_%(table_name)s_%(column_0_name)s",
			"ck": "ck_%(table_name)s_`%(constraint_name)s`",
			"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
			"pk": "pk_%(table_name)s",
		},
	)

	type_annotation_map = {datetime.datetime: DateTime(timezone=True)}


engine = create_async_engine(
	settings.DATABASE_URL,
	echo=settings.SQLALCHEMY_ECHO,
)

async_session_maker = async_sessionmaker(
	autoflush=False,
	autocommit=False,
	bind=engine,
)


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
	async with async_session_maker() as db:
		yield db


DBSession = Annotated[AsyncSession, Depends(get_async_db_session)]
