import aiohttp
from pydantic_settings import BaseSettings, SettingsConfigDict


class JiraConfig(BaseSettings):
    JIRA_BASE_URL: str
    JIRA_USERNAME: str
    JIRA_API_TOKEN: str
    JIRA_PROJECT_ID: str

    model_config = SettingsConfigDict(env_file=".env")


def get_api_headers():
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
