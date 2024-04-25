""" Configuration module for the Jira API. """

from pydantic_settings import BaseSettings, SettingsConfigDict


class JiraConfig(BaseSettings):
    """
    Configuration class for the Jira API. Carries the necessary settings for
    interacting with the Jira API.
    """

    JIRA_BASE_URL: str
    JIRA_USERNAME: str
    JIRA_API_TOKEN: str
    JIRA_PROJECT_ID: str

    model_config = SettingsConfigDict(env_file=".env")


def get_api_headers():
    """
    Get the API headers for the Jira API.
    :return: dict
    """
    return {
        "Content-Type": "application/json",
    }
