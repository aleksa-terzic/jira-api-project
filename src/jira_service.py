"""
JiraService class that implements methods used to interact with Jira API.

Currently, it includes methods to create a ticker and get create metadata for tickets.
The class uses aiohttp to perform asynchronous HTTP requests to the Jira API.
It is initialized with the necessary configuration params.

Example usage:
    jira_service = JiraService()
    response = await jira_service.create_ticket(jira_ticket, webhook_url)
    issue_types = await jira_service.get_issue_types()
"""

import asyncio
import json
import typing

import aiohttp
from fastapi import status
from pydantic import ValidationError

from src.schemas import ticket as ticket_model
from src.schemas import errors as error_model
from src.utils import configuration

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
        Perform a GET request to Jira API.

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
        Perform a POST request to Jira API.

        :param endpoint: str
        :param data: dict
        :param session: aiohttp.ClientSession
        :return: dict
        """
        async with session.post(
            endpoint, json=data, auth=self.auth, headers=self.headers
        ) as response:
            return await _handle_response(response)

    async def _create_ticket(
        self,
        jira_ticket: ticket_model.TicketData,
        webhook_url: str,
        session: aiohttp.ClientSession,
    ) -> dict:
        """
        Create a Jira ticket and send a webhook notification to the user with the result.

        :param jira_ticket: TicketData
        :param webhook_url: str - URL to send the notification to
        :return: dict
        """
        endpoint = f"{self.base_url}{self.JIRA_ISSUE_CREATE_ENDPOINT}"
        # Construct the data payload for the ticket creation
        data = {
            "fields": {
                "project": {"id": self.project_id},
                "summary": jira_ticket.summary,
                "description": jira_ticket.description,
                "issuetype": {"id": jira_ticket.issue_type},
            }
        }
        try:
            response = await self._post(endpoint, data, session)

            # Extract ticket ID from the response and send a webhook notification
            ticket_id = response.get("id") if response else None
            await send_webhook_notification(
                webhook_url, success=True, ticket_id=ticket_id
            )
            return response
        # We still want to send a webhook notification if an exception occurs,
        # so we catch all exceptions here and send the notification
        # before re-raising the exception.
        except Exception as ex:
            error_message = str(ex)

            # Send a webhook notification with the error message
            await send_webhook_notification(
                webhook_url, success=False, error=error_message
            )
            raise ex

    async def create_tickets(self, tickets: ticket_model, webhook_url: str):
        """
        Create one or multiple Jira tickets. Calls the _create_ticket method for each
        ticket in the list.
        Not the most efficient way to create multiple tickets, there is an endpoint
        for bulk ticket creation in Jira API.

        :param webhook_url:
        :param tickets: list of TicketsCreate
        :return: list of responses from Jira API containing ticket data
        """
        async with aiohttp.ClientSession() as session:
            tasks = [
                self._create_ticket(ticket, webhook_url, session) for ticket in tickets
            ]
            responses = await asyncio.gather(*tasks)
            return {"tickets": responses}

    async def get_issue_types(self) -> dict:
        """
        Get all available issue types of a project in Jira.

        :return: dict containing issue types information
        """
        endpoint = f"{self.base_url}{self.JIRA_ISSUE_CREATEMETA_ENDPOINT}"
        async with aiohttp.ClientSession() as session:
            return await self._get(endpoint, session)


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


def _handle_jira_error(error_message) -> typing.Union[str, dict]:
    """
    Handle Jira error message. TODO: Needs more detailing.

    :param error_message: str
    :return: str
    """
    try:
        error_data = json.loads(error_message)
        jira_error = error_model.JiraError.parse_obj(
            error_data
        )  # Parse JSON into JiraError object
        error_detail = (
            f"Status: {jira_error.status}, Messages: {', '.join(jira_error.errors)}"
        )
    except (json.JSONDecodeError, ValidationError):
        error_detail = error_message
    return error_detail


async def send_webhook_notification(
    webhook_url: str, success: bool, ticket_id: str = None, error: str = None
) -> None:
    """
    Send a webhook notification to user with the result of the ticket creation.
    Usually should be called as a background task.

    :param webhook_url: str - URL to send the notification to
    :param success: bool - whether the ticket was created successfully
    :param ticket_id: str - ID of the created ticket if available
    :param error: str - error message if ticket creation failed
    :return: None
    """
    payload = {"success": success, "ticket_id": ticket_id, "error": error}

    async with aiohttp.ClientSession() as session:
        await session.post(webhook_url, json=payload)
