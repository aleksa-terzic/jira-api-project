"""
Database imitation module for authentication.

Contains functions that imitate database queries for authentication purposes and
has predefined data for demonstration purposes.
Usually you would opt to have a real database such as PostgreSQL.
"""

users = {
    "aleksa_rivian": {"name": "Aleksa", "webhook_url": "http://localhost:8000/webhook"},
    "sara_rivian": {"name": "Sara", "webhook_url": "http://localhost:8000/webhook"},
    "natasa_rivian": {"name": "Natasa", "webhook_url": "http://localhost:8000/webhook"},
}

# 32bit api key length for demonstration purposes
api_keys = {
    "4BwWbVFpCaikFZe8G8rr7I21nhCw8N0t": "aleksa_rivian",
    "jWxSZ9gtZ7waoIinQRKVf5hvAcEVIt9c": "sara_rivian",
    "jpjHQvZHdyXjKdpKbTEUZPesnZrjvrvl": "natasa_rivian",
}


def check_api_key(api_key: str) -> bool:
    """
    Check if the API key is valid.
    :param api_key: str
    :return: boolean
    """
    return api_key in api_keys


def get_user_from_api_key(api_key: str) -> dict:
    """
    Get the user from the API key.
    :param api_key: str
    :return: dict with user data
    """
    return users[api_keys[api_key]]
