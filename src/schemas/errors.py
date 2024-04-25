""" Pydantic models for Jira error response. """

from typing import Any, Dict, List

from pydantic import BaseModel


class JiraError(BaseModel):
    """
    Pydantic model for Jira error response.
    """

    errorMessages: List[str]
    errors: Dict[str, Any]
    status: int
