""" JiraService class that implements methods used to interact with Jira API."""

import json

import aiohttp
from fastapi import status

from src import configuration
from src.schemas.ticket import TicketData

# Initialize configuration
config = configuration.JiraConfig()


class JiraService:
    """
    JiraService class with methods to interact with Jira API.
    """

    JIRA_ISSUE_CREATE_ENDPOINT = "/rest/api/3/issue"
    JIRA_ISSUE_CREATEMETA_ENDPOINT = "/rest/api/3/issue/createmeta"

    def __init__(self):
        self.base_url = config.JIRA_BASE_URL
        self.username = config.JIRA_USERNAME
        self.api_token = config.JIRA_API_TOKEN
        self.project_id = config.JIRA_PROJECT_ID
        self.auth = aiohttp.BasicAuth(self.username, self.api_token)
        self.headers = configuration.get_api_headers()

    async def _get(self, endpoint, session) -> dict:
        """
        Perform a GET request to Jira API
        :param endpoint: str
        :param session: aiohttp.ClientSession
        :return: dict
        """
        async with session.get(
            endpoint, auth=self.auth, headers=self.headers
        ) as response:
            return await _handle_response(response)

    async def _post(self, endpoint, data, session) -> dict:
        """
        Perform a POST request to Jira API
        :param endpoint: str
        :param data: dict
        :param session: aiohttp.ClientSession
        :return: dict
        """
        async with session.post(
            endpoint, json=data, auth=self.auth, headers=self.headers
        ) as response:
            return await _handle_response(response)

    async def create_ticket(self, ticket: TicketData) -> dict:
        """
        Private method to create a Jira ticket, called from create_tickets
        :param ticket: TicketData
        :return: dict
        """
        endpoint = f"{self.base_url}{self.JIRA_ISSUE_CREATE_ENDPOINT}"
        data = {
            "fields": {
                "project": {"id": self.project_id},
                "summary": ticket.summary,
                "description": ticket.description,
                "issuetype": {"id": ticket.issue_type},
            }
        }
        async with aiohttp.ClientSession() as session:
            return await self._post(endpoint, data, session)

    async def get_issue_types(self) -> dict:
        """
        Get issue types for a project
        :return: dict
        """
        endpoint = f"{self.base_url}{self.JIRA_ISSUE_CREATEMETA_ENDPOINT}"
        async with aiohttp.ClientSession() as session:
            return await self._get(endpoint, session)

    # async def create_tickets(self, tickets):
    #     """
    #     Create Jira tickets
    #     :param tickets: list of TicketsCreate
    #     :return: list of responses
    #     """
    #     async with aiohttp.ClientSession() as session:
    #         tasks = [self._create_ticket(ticket, session) for ticket in tickets]
    #         responses = await asyncio.gather(*tasks)
    #         return responses


async def _handle_response(response) -> dict:
    """
    Handle response from Jira API
    :param response: dict
    :return: dict
    """
    if response.status in {status.HTTP_200_OK, status.HTTP_201_CREATED}:
        return await response.json()
    error_message = await response.text()
    error_detail = _handle_jira_error(error_message)
    return {"error": f"Request failed: {error_detail}"}


def _handle_jira_error(error_message) -> str:
    """
    Handle Jira error message
    :param error_message: str
    :return: str
    """
    try:
        error_data = json.loads(error_message)
        error_detail = error_data.get("errors", error_message)
    except json.JSONDecodeError:
        error_detail = error_message
    return error_detail
