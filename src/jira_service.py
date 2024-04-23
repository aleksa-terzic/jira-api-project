import asyncio
import json

import aiohttp
from src import configuration

config = configuration.JiraConfig()


class JiraService:
    def __init__(self):
        self.base_url = config.JIRA_BASE_URL
        self.username = config.JIRA_USERNAME
        self.api_token = config.JIRA_API_TOKEN
        self.project_id = config.JIRA_PROJECT_ID
        self.auth = aiohttp.BasicAuth(self.username, self.api_token)
        self.headers = configuration.get_api_headers()

    async def _get(self, endpoint, session):
        """
        Perform a GET request to Jira API
        :param endpoint:
        :param session:
        :return:
        """
        async with session.get(
            endpoint, auth=self.auth, headers=self.headers
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_message = await response.text()
                error_detail = _handle_jira_error(error_message)
                return {"error": f"Failed to perform GET request: {error_detail}"}

    async def _post(self, endpoint, data, session):
        """
        Perform a POST request to Jira API
        :param endpoint:
        :param data:
        :param session:
        :return:
        """
        async with session.post(
            endpoint, json=data, auth=self.auth, headers=self.headers
        ) as response:
            if response.status == 201:
                return await response.json()
            else:
                error_message = await response.text()
                error_detail = _handle_jira_error(error_message)
                return {"error": f"Failed to perform POST request: {error_detail}"}

    async def _create_ticket(self, ticket, session):
        """
        Private method to create a Jira ticket, called from create_tickets
        :param ticket:
        :param session:
        :return:
        """
        path = "/rest/api/3/issue"
        endpoint = f"{self.base_url}{path}"  # use pydantic model for this
        data = dict(
            fields=dict(
                project=dict(id=self.project_id),
                summary=ticket.summary,
                description=ticket.description,
                issuetype=dict(id=ticket.issue_type),
            )
        )
        return await self._post(endpoint, data, session)

    async def create_tickets(self, tickets):
        """
        Create Jira tickets
        :param tickets: list of TicketsCreate
        :return: list of responses
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self._create_ticket(ticket, session) for ticket in tickets]
            responses = await asyncio.gather(*tasks)
            return responses

    async def get_issue_types(self):
        """
        Get issue types for a project
        :return: dict
        """
        path = "/rest/api/3/issue/createmeta"
        endpoint = f"{self.base_url}{path}"
        async with aiohttp.ClientSession() as session:
            return await self._get(endpoint, session)


def _handle_jira_error(error_message):
    """
    Handle Jira error message
    :param error_message:
    :return:
    """
    try:
        error_data = json.loads(error_message)
        error_detail = error_data.get("errors", error_message)
    except json.JSONDecodeError:
        error_detail = error_message
    return error_detail
