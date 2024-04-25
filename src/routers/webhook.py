"""
Webhook router, which is responsible for handling webhook notifications.

It contains only a demonstration endpoint that will print the payload
to the standard output.
"""

import sys

import fastapi

router = fastapi.APIRouter()


@router.post("/webhook")
async def receive_webhook(request: fastapi.Request):
    """
    Endpoint to receive webhook notifications - for demonstration purposes only.
    It will print the payload to the standard output.
    """
    data = await request.json()
    sys.stdout.write("Received webhook payload:")
    # Even though sys.stdout.write is synchronous, reading the request payload
    # is asynchronous, so it can handle multiple concurrent requests without blocking.
    sys.stdout.write(str(data))
