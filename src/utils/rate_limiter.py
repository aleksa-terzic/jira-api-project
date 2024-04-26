"""
Rate limiter middleware that applies rate limiting checks to incoming requests.

Implements a simple fixed rate limiter that allows a fixed number of requests
per window.
This could be improved by implementing leaky bucket or token bucket algorithms.

RateLimiter: Rate limiter class that uses Redis to store the current amount of requests.
RateLimitMiddleware: Rate limiting middleware that applies rate limiting checks
to incoming requests.
"""

import json
from typing import Callable

import redis
from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimiter:
    """Rate limiter class that uses Redis to store the current amount of requests."""

    def __init__(self):
        self.redis = None

    async def init_redis(self):
        """Initialize the Redis connection."""
        self.redis = await redis.asyncio.from_url("redis://my-redis")

    async def get_rate_limit_key(self, request: Request) -> str:  # noqa
        """
        Generate a key for rate limiting based on the user's IP address.

        :param request: Request object
        :return: str key for rate limiting
        """
        return request.client.host


class RateLimitMiddleware(BaseHTTPMiddleware):  # pylint: disable=too-few-public-methods
    """
    Rate limiting middleware that applies rate limiting checks to incoming requests.
    Implements a simple fixed rate limiter that allows
    a fixed number of requests per window.
    This could be improved by implementing leaky bucket or token bucket algorithms.
    """

    def __init__(self, app: Callable, window: int = 60, limit: int = 60):
        # Default rate limit of 60 requests per minute per IP address.
        super().__init__(app)
        self.window = window
        self.limit = limit
        self.limiter = RateLimiter()

    async def dispatch(self, request: Request, call_next):
        await self.limiter.init_redis()
        client = self.limiter.redis
        key = await self.limiter.get_rate_limit_key(request)

        try:
            current_requests = await client.incr(key)
            if current_requests == 1:
                await client.expire(key, self.window)

            if int(current_requests) > self.limit:
                error_detail = "Rate limit exceeded, slow down!"
                return Response(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content=json.dumps({"detail": error_detail}),
                    media_type="application/json",
                )

            response = await call_next(request)
            return response

        finally:
            await client.aclose()
