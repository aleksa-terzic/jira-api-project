from fastapi import FastAPI

from src.routers import ticket

app = FastAPI()

app.include_router(ticket.router)
