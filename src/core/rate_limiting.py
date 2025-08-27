from collections.abc import Callable
from typing import Any, TypeVar

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

T = TypeVar("T", bound=Callable[..., Any])


def rate_limit(limit_value: str) -> Callable[[T], T]:
	"""
	Type-safe decorator to apply rate limiting to FastAPI route handlers.
	"""

	def decorator(func: T) -> T:
		return limiter.limit(limit_value)(func)  # type: ignore[reportUnknownVariableType]

	return decorator
