from fastapi import FastAPI

from src.routers import ticket

app = FastAPI()

app.include_router(ticket.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
