from fastapi import FastAPI
import os
from dotenv import load_dotenv
import aiohttp

app = FastAPI()

# Load environment variables
load_dotenv()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


auth = aiohttp.BasicAuth(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
url = "https://your-domain.atlassian.net/rest/api/3/issue"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

payload = {
    "fields": {
        "project": {
            "id": "10000"
        },
        "summary": "Test Summary",
        "description": "Test Description",
        "issuetype": {
            "name": "Task"
        }
    }
}

createmeta_url = "https://your-domain.atlassian.net/rest/api/3/issue/createmeta"
c_headers = {
  "Accept": "application/json"
}

@app.post("/generate")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
