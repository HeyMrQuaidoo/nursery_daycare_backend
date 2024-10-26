import threading

from app.db.dbModule import DBModule
from app.core.config import settings


class DBManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls, *args, **kwargs)
                    cls._instance._db_module = None
        return cls._instance

    @property
    def db_module(self):
        if self._db_module is None:
            self._initialize_db_module()
        return self._db_module

    def _get_credentials_from_env(self):
        return {
            "user": settings.DB_USER,
            "pswd": settings.DB_PASSWORD,
            "host": settings.DB_HOST,
            "port": settings.DB_PORT,
            "db": settings.DB_DATABASE,
            "engine": settings.DB_ENGINE,
        }

    def _initialize_db_module(self):
        if self._db_module is None:
            credentials = self._get_credentials_from_env()
            try:
                self._db_module = DBModule(**credentials)
            except Exception as e:
                raise RuntimeError(f"Failed to initialize DBModule: {e}")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
