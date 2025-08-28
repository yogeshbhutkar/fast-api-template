from fastapi import FastAPI

<<<<<<< HEAD:src/core/api.py
from src.auth.controller import router as auth_router
from src.todos.controller import router as todos_router
from src.users.controller import router as users_router
from src.langfuse.controller import router as langfuse_router
=======
from app.auth.controller import router as auth_router
from app.todos.controller import router as todos_router
from app.users.controller import router as users_router
>>>>>>> main:app/core/api.py


def register_routes(app: FastAPI):
	app.include_router(todos_router)
	app.include_router(auth_router)
	app.include_router(users_router)
	app.include_router(langfuse_router)
