# import redis
import redis.asyncio as redis
from typing import Any, Optional


class CacheModule:
    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: Optional[str] = None,
        **kwargs,
    ):
        self.host = host
        self.port = port
        self.password = password
        self.user = user
        self.redis = None

    async def connect(self):
        print("Trying to connect to Redis")

        self.redis = redis.Redis(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            ssl=True,
            ssl_cert_reqs=None,
            decode_responses=True,
        )

    async def disconnect(self):
        if self.redis:
            await self.redis.close()
            await (
                self.redis.connection_pool.disconnect()
            )  # Disconnect the connection pool
            self.redis = None

    async def set(self, key: str, value: Any, expire: Optional[int] = None):
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        await self.redis.set(key, value, ex=expire)

    async def get(self, key: str) -> Optional[Any]:
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        return await self.redis.get(key)

    async def delete(self, key: str):
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        return await self.redis.exists(key)

    async def clear_all(self):
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        await self.redis.flushdb()

    def __del__(self):
        if self.redis:
            self.redis.close()
