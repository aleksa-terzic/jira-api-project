""" Pydantic models for ticket data. """

import typing

import pydantic


class ContentItem(pydantic.BaseModel):
    """Part of a paragraph."""

    type: str
    text: str


class Paragraph(pydantic.BaseModel):
    """A paragraph in description."""

    type: str
    content: typing.List[ContentItem]


class Description(pydantic.BaseModel):
    """Description of a ticket."""

    type: str
    version: int
    content: typing.List[Paragraph]


class TicketData(pydantic.BaseModel):
    """Data for creating a ticket."""

    summary: str
    description: str
    issue_type: str

    @pydantic.field_validator("description")
    def validate_description(cls, value):  # pylint: disable=no-self-argument
        """Validates and calls to convert description to Jira JSON format."""
        if isinstance(value, str):
            return cls._convert_description_to_json_format(value)
        return value

    @staticmethod
    def _convert_description_to_json_format(description_text):
        """
        Splits the description text into paragraphs and
        converts to Jira JSON format.
        """
        paragraphs = description_text.splitlines()

        content = []
        for paragraph_text in paragraphs:
            content_item = ContentItem(type="text", text=paragraph_text.strip())
            paragraph = Paragraph(type="paragraph", content=[content_item])
            content.append(paragraph)

        description_json = {"type": "doc", "version": 1, "content": content}
        return Description(**description_json).dict()


class TicketsCreateResponse(pydantic.BaseModel):
    """Response for ticket creation."""

    id: str
    key: str
    self: str


# class TicketsCreate(BaseModel):
#     tickets: List[TicketData]


class Project(pydantic.BaseModel):
    """Jira project."""

    id: str
    key: str
    name: str


class IssueType(pydantic.BaseModel):
    """Jira issue type details."""

    id: str
    description: str
    name: str


class ProjectDetails(pydantic.BaseModel):
    """Details of a Jira project along with issue types available."""

    project: Project
    issue_types: typing.List[IssueType]
