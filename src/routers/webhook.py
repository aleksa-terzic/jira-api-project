"""
Webhook router, which is responsible for handling webhook notifications.

It contains only a demonstration endpoint that will print the payload
to the standard output.
"""

import sys

import fastapi

router = fastapi.APIRouter()


@router.post("/webhook")
async def receive_webhook(payload: dict):
    """
    Endpoint to receive webhook notifications - for demonstration purposes only.
    It will print the payload to the standard output.
    """
    if not payload:
        return
    sys.stdout.write("Received webhook payload:")
    sys.stdout.write(str(payload))
