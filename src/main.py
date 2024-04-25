"""Main module for the FastAPI application."""

import fastapi
from starlette.middleware import cors

from src.routers import ticket

app = fastapi.FastAPI()

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ticket.router)
