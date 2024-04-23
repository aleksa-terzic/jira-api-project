from fastapi import APIRouter, HTTPException

from src.jira_service import JiraService
from src.schemas.ticket import TicketsCreate, IssueType, ProjectDetails, Project

router = APIRouter()
jira_service = JiraService()


# create pydantic model for response?? response_model=TicketsCreateResponse
@router.post("/generate")
async def create_tickets(ticket_data: TicketsCreate):
    tickets = ticket_data.tickets
    responses = await jira_service.create_tickets(tickets)
    return responses


@router.get("/issuetypes")
async def get_issue_types():
    jira_response = await jira_service.get_issue_types()

    selected_project = next(
        (
            project
            for project in jira_response["projects"]
            if project["id"] == "10000"  # use config.JIRA_PROJECT_ID
        ),
        None,
    )
    if selected_project:
        # Extract relevant project information
        formatted_project = Project(
            id=selected_project["id"],
            key=selected_project["key"],
            name=selected_project["name"],
        )

        # Extract issue types for the selected project
        issue_types = []
        for issue_type in selected_project["issuetypes"]:
            issue_types.append(
                IssueType(
                    id=issue_type["id"],
                    description=issue_type["description"],
                    name=issue_type["name"],
                )
            )

        # Construct response data
        response_data = ProjectDetails(
            project=formatted_project, issue_types=issue_types
        )
        return response_data
    else:
        raise HTTPException(status_code=404, detail="Project not found")
