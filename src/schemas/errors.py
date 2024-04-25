""" Pydantic models for Jira error response. """

import typing

import pydantic


class JiraError(pydantic.BaseModel):
    """
    Pydantic model for Jira error response.
    """

    errorMessages: typing.List[str]
    errors: typing.Dict[str, typing.Any]
    status: int
