""" Database imitation module for authentication. """

# 32bit api key length for demonstration purposes
api_keys = {
    "4BwWbVFpCaikFZe8G8rr7I21nhCw8N0t": "aleksa_rivian",
    "jWxSZ9gtZ7waoIinQRKVf5hvAcEVIt9c": "sara_rivian",
    "jpjHQvZHdyXjKdpKbTEUZPesnZrjvrvl": "natasa_rivian",
}

users = {
    "aleksa_rivian": {"name": "Aleksa"},
    "sara_rivian": {"name": "Sara"},
    "natasa_rivian": {"name": "Natasa"},
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
