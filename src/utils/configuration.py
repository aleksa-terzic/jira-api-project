"""
Configuration module for the Jira API.

Contains the configuration class for the Jira API and a function to get the
API headers.
"""

import pydantic_settings


class JiraConfig(pydantic_settings.BaseSettings):
    """
    Configuration class for the Jira API. Carries the necessary settings for
    interacting with the Jira API.
    """

    JIRA_BASE_URL: str
    JIRA_USERNAME: str
    JIRA_API_TOKEN: str
    JIRA_PROJECT_ID: str

    # Load env variables from .env
    model_config = pydantic_settings.SettingsConfigDict(env_file=".env")


def get_api_headers():
    """
    Get the API headers for the Jira API.
    :return: dict
    """
    return {
        "Content-Type": "application/json",
    }
