from fastapi import APIRouter

from src.jira_service import JiraService
from src.schemas.ticket import TicketsCreate

router = APIRouter()
jira_service = JiraService()


@router.post("/generate")
async def create_tickets(ticket_data: TicketsCreate):
    tickets = ticket_data.tickets
    responses = await jira_service.create_tickets(tickets)
    return responses
