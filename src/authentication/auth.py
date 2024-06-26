""" Authentication logic for our API. Implements basic API key authentication. """

from fastapi import HTTPException, Security, security, status

from src.authentication import db

api_key_header = security.APIKeyHeader(name="X-API-Key")


def get_user(key_header: str = Security(api_key_header)):
    """
    Get the user from the API key provided in the header.
    :param key_header: str
    :return: dict with user data
    """
    if db.check_api_key(key_header):
        user = db.get_user_from_api_key(key_header)
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid API key"
    )
