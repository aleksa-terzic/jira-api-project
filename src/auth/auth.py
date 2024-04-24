from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from src.auth.db import check_api_key, get_user_from_api_key

api_key_header = APIKeyHeader(name="X-API-Key")


def get_user(key_header: str = Security(api_key_header)):
    """
    Get the user from the API key provided in the header.
    :param key_header: str
    :return: dict with user data
    """
    if check_api_key(key_header):
        user = get_user_from_api_key(key_header)
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid API key"
    )
