import threading
import asyncio

from app.cache.cacheModule import CacheModule
from app.core.config import settings


class CacheManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls, *args, **kwargs)
                    cls._instance._cache_module = None
        return cls._instance

    @property
    def cache_module(self):
        if self._cache_module is None:
            asyncio.run(self._initialize_cache_module())
        return self._cache_module

    def _get_cache_credentials_from_env(self):
        return {
            "host": settings.CACHE_HOST,
            "port": settings.CACHE_PORT,
            "user": settings.CACHE_USER,
            "password": settings.CACHE_PASSWORD,
        }

    async def _initialize_cache_module(self):
        if self._cache_module is None:
            credentials = self._get_cache_credentials_from_env()
            try:
                self._cache_module = CacheModule(**credentials)
                print(f"Cache has been set {self._cache_module}")
                await self._cache_module.connect()  # Establish a connection
            except Exception as e:
                raise RuntimeError(f"Failed to initialize CacheModule: {e}")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
