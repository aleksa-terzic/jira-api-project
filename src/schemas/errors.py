from pydantic import BaseModel
from typing import List, Dict, Any


class JiraError(BaseModel):
    errorMessages: List[str]
    errors: Dict[str, Any]
    status: int
