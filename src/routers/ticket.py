""" This module contains the FastAPI router for ticket-related endpoints. """

from fastapi import APIRouter, Depends, HTTPException, status

from src.authentication import auth
from src import configuration
from src import jira_service as service
from src.schemas import ticket

router = APIRouter()
jira_service = service.JiraService()
jira_config = configuration.JiraConfig()


# create pydantic model for response?? response_model=TicketsCreateResponse
@router.post(
    "/generate",
    response_model=ticket.TicketsCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_tickets(ticket_data: ticket.TicketData, _=Depends(auth.get_user)):
    """
    Creates a ticket in Jira project.
    Can create multiple tickets at once.
    """
    # tickets = ticket_data.tickets
    responses = await jira_service.create_ticket(ticket_data)
    return responses


@router.get(
    "/issue-types", response_model=ticket.ProjectDetails, status_code=status.HTTP_200_OK
)
async def get_issue_types(_=Depends(auth.get_user)):
    """
    Gets all issue types available for the selected project.
    You set up the project ID in the .env file.
    """
    jira_response = await jira_service.get_issue_types()

    selected_project = next(
        (
            project
            for project in jira_response["projects"]
            if project["id"] == jira_config.JIRA_PROJECT_ID
        ),
        None,
    )
    if selected_project:
        # Extract relevant project information
        formatted_project = ticket.Project(
            id=selected_project["id"],
            key=selected_project["key"],
            name=selected_project["name"],
        )

        # Extract issue types for the selected project
        issue_types = []
        for issue_type in selected_project["issuetypes"]:
            issue_types.append(
                ticket.IssueType(
                    id=issue_type["id"],
                    description=issue_type["description"],
                    name=issue_type["name"],
                )
            )

        # Construct response data
        response_data = ticket.ProjectDetails(
            project=formatted_project, issue_types=issue_types
        )
        return response_data
    raise HTTPException(status_code=404, detail="Project not found")
