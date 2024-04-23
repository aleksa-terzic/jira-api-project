from typing import List

from pydantic import BaseModel, field_validator


class ContentItem(BaseModel):
    type: str
    text: str


class Paragraph(BaseModel):
    type: str
    content: List[ContentItem]


class Description(BaseModel):
    type: str
    version: int
    content: List[Paragraph]


class TicketData(BaseModel):
    summary: str
    description: str
    issue_type: str

    @field_validator("description")
    def validate_description(cls, value):
        if isinstance(value, str):
            return cls._convert_description_to_json_format(value)
        return value

    @staticmethod
    def _convert_description_to_json_format(description_text):
        paragraphs = description_text.splitlines()

        content = []
        for paragraph_text in paragraphs:
            content_item = ContentItem(type="text", text=paragraph_text.strip())
            paragraph = Paragraph(type="paragraph", content=[content_item])
            content.append(paragraph)

        description_json = {"type": "doc", "version": 1, "content": content}
        return Description(**description_json).dict()


class TicketsCreate(BaseModel):
    tickets: List[TicketData]


class Project(BaseModel):
    id: str
    key: str
    name: str


class IssueType(BaseModel):
    id: str
    description: str
    name: str


class ProjectDetails(BaseModel):
    project: Project
    issue_types: List[IssueType]
