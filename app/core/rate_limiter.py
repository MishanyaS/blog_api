from fastapi import HTTPException, status, Request
from app.core.redis import redis_client
import time

class RateLimiter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
    
    async def __call__(self, request: Request):
        identifier = await self._get_identifier(request)
        
        window = int(time.time() // self.window)
        key = f"rate:{identifier}:{window}"
        
        current = await redis_client.incr(key)
        
        if current == 1:
            await redis_client.expire(key, self.window)
        
        if current > self.limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests",
            )
    
    async def _get_identifier(self, request: Request) -> str:
        auth = request.headers.get("authorization")
        
        if auth and auth.startswith("Bearer "):
            from app.core.security import decode_token
            
            token = auth.split(" ")[1]
            try:
                payload = decode_token(token)
                return f"user:{payload('sub')}"
            except Exception:
                pass
        
        client_ip = request.client.host
        return f"ip:{client_ip}"