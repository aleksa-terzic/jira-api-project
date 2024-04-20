import json

import aiohttp
from src import configuration

config = configuration.JiraConfig()


class JiraService:
    def __init__(self):
        self.base_url = config.JIRA_BASE_URL
        self.username = config.JIRA_USERNAME
        self.api_token = config.JIRA_API_TOKEN
        self.project_id = config.JIRA_PROJECT_ID
        self.auth = aiohttp.BasicAuth(self.username, self.api_token)
        self.headers = configuration.get_api_headers()

    async def create_ticket(self, summary, description):
        path = "/rest/api/3/issue"
        endpoint = f"{self.base_url}{path}"
        data = dict(
            fields=dict(
                project=dict(id=self.project_id),
                summary=summary,
                description=description,
                issuetype=dict(id="10002"),
            )
        )

        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint, json=data, auth=self.auth, headers=self.headers
            ) as response:
                if response.status == 201:
                    return await response.json()
                else:
                    error_message = await response.text()
                    try:
                        error_data = json.loads(error_message)
                        error_detail = error_data.get("errors", error_message)
                    except json.JSONDecodeError:
                        error_detail = error_message
                    return {"error": f"Failed to create Jira ticket: {error_detail}"}
