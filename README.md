# FastAPI Jira API

This project implements a FastAPI-based API for interacting with the Jira REST API. It provides endpoints to perform operations on Jira issues.

## Features

- **Authentication**: Utilizes API tokens for secure access to the API.
- **Endpoints**: Offers endpoints to create Jira issues.
- **Validation**: Input validation and error handling are integrated into the API endpoints.
- **Asynchronous**: Supports asynchronous request handling using FastAPI's async capabilities.
- **Dockerized**: The application is containerized using Docker for easy deployment.
- **Webhooks**: Demonstrates how to receive webhooks from our own API.
- **Rate Limiting**: Implements rate limiting to prevent abuse of the API.
  
## Requirements

- Python 3.9
- Jira API access (URL, credentials/token)
- Docker

How to manage API tokens for your Atlassian account [here](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/).
  
## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/aleksa-terzic/jira-api-project.git
   ```
   
2. Set up your Jira API credentials in the .env file (see .env-example for reference):

   ```bash
   JIRA_URL=https://your-jira-url.atlassian.net
   JIRA_USERNAME=your-email-address-from-jira
   JIRA_API_TOKEN=your-jira-api-token
   JIRA_PROJECT_ID=your-jira-project-id
   ```

3. Build the Docker image and run the container:

   ```bash
    docker-compose up --build
    ```
   
4. Make sure to grab one of the API keys from `src/authentication/db.py` and use it as the `x-api-key` header in your requests.
   
You can now access the API at http://localhost:8000/docs.
   

## Endpoints

- `GET /issue-types`: Retrieve a list of issue types available for creation in the Jira project.
- `POST /generate`: Create a new ticket/tickets in the Jira project.
- `POST /webhook`: Receive a webhook from our own API for demonstration purposes.