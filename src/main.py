"""Main module for the FastAPI application."""

import fastapi
from starlette.middleware import cors

from src.routers import ticket, webhook


def get_application():
    """
    Initialize the FastAPI application and add the routers.
    :return: FastAPI application
    """
    application = fastapi.FastAPI()
    application.add_middleware(
        cors.CORSMiddleware,  # noqa
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(ticket.router)
    application.include_router(webhook.router)

    return application


app = get_application()
