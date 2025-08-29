import inngest.fast_api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ai.service import generate_response
from app.core.adapters.inngest import inngest_client
from app.core.api import register_routes
from app.core.config import settings
from app.core.logger import LogLevels, configure_logging

configure_logging(log_level=LogLevels.info)

app = FastAPI(
	title="FastAPI Template",
	description="An all batteries included template for FastAPI.",
	version="0.1.0",
	docs_url="/docs",
	redoc_url="/redoc",
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.ALLOWED_ORIGINS,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

register_routes(app)

# Register Inngest functions.
inngest.fast_api.serve(app, inngest_client, [generate_response])

if __name__ == "__main__":
	import uvicorn

	uvicorn.run(
		app="app.main:app",
		host="0.0.0.0",
		port=8000,
		reload=True,
	)
