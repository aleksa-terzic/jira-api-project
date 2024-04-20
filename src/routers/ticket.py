from fastapi import APIRouter

from src.jira_service import JiraService
from src.schemas.ticket import TicketCreate

router = APIRouter()
jira_service = JiraService()


@router.post("/generate")
async def create_ticket(ticket_data: TicketCreate):
    summary = ticket_data.summary
    description = ticket_data.description

    response = await jira_service.create_ticket(summary, description)
    return response
