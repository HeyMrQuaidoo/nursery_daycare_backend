from urllib.parse import quote
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from typing import Any, TypeVar, AsyncIterator
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import sessionmaker


from app.core.config import settings
from app.db.dbDeclarative import Base
import app.core.errors as DBExceptions


class DBModule:
    _base: Any = Base
    T = TypeVar("T", bound=Base)
    _models_generated: bool = False

    def __init__(self, **kwargs):
        self.credentials = kwargs

        # create database engine
        self.engine_type = kwargs.get("engine", "postgres")
        self.engine_setup_func = self.get_engine_setup_func(self.engine_type)
        self.engine: AsyncEngine = self.engine_setup_func(self.credentials)

        # create session
        self.Session: AsyncSession = async_sessionmaker(
            autocommit=False,
            expire_on_commit=False,
            autoflush=True,
            bind=self.engine["write"],
            class_=AsyncSession,
        )

        # sync connection
        user = self.credentials.get("user")
        pswd = self.credentials.get("pswd", "")
        host = self.credentials.get("host")
        port = self.credentials.get("port", 3306)
        db = self.credentials.get("db")

        # create synchronous session
        # TODO: review if this is necessary
        self.SyncSessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=create_engine(
                f"postgresql://{user}:{quote(pswd)}@{host}:{port}/{db}", echo=False
            ),
        )

    @classmethod
    def get_declarative_base(self):
        return self._base

    async def get_db(self) -> AsyncIterator[AsyncSession]:
        async with self.Session() as session:
            yield session

    def get_sync_db(self):
        return self.SyncSessionLocal()

    def get_engine(self):
        return self.engine

    def dispose(self):
        self.engine["write"].dispose()

    async def check_models_generated(self):
        if not self._models_generated:
            await self.create_all_tables()
            self._models_generated = True

    def get_engine_setup_func(cls, engine):
        supporting_rdbms = {
            "postgres": cls.setup_postgres,
            "mysql": cls.setup_mysql,
            "sqlite": cls.setup_sqlite,
            "memory": cls.setup_memory,
        }
        return supporting_rdbms.get(engine, cls.setup_sqlite)

    def setup_postgres(cls, credentials: dict):
        user = credentials.get("user")
        pswd = credentials.get("pswd", "")
        host = credentials.get("host")
        port = credentials.get("port", 3306)
        db = credentials.get("db")
        conn_string = f"postgresql+asyncpg://{user}:{quote(pswd)}@{host}:{port}/{db}"

        # create database if it doesn't exist
        cls.create_postgres_database_if_not_exist(conn_string)

        if not all([user, host, db]):
            raise DBExceptions.DatabaseCredentialException(
                "DB, USER and HOST are required"
            )

        return {
            "write": create_async_engine(conn_string, future=True, echo=False),
            "read": create_async_engine(conn_string, future=True, echo=False),
        }

    def setup_mysql(cls, credentials: dict):
        user = credentials.get("user")
        pswd = credentials.get("pswd", "")
        host = credentials.get("host")
        read_host = credentials.get("read_host", host)
        port = credentials.get("port", 3306)
        db = credentials.get("db")

        if not all([user, host, db]):
            raise DBExceptions.DatabaseCredentialException(
                "DB, USER and HOST are required"
            )

        return {
            "write": create_async_engine(
                f"mysql+asyncmy://{user}:{quote(pswd)}@{host}:{port}/{db}",
                future=True,
                echo=False,
            ),
            "read": create_async_engine(
                f"mysql+asyncmy://{user}:{quote(pswd)}@{read_host}:{port}/{db}",
                future=True,
                echo=False,
            ),
        }

    def setup_memory(cls, credentials=":memory:"):
        return {
            "write": create_async_engine(
                f"sqlite+pysqlite:///{credentials}", future=True, echo=True
            ),
            "read": create_async_engine(
                f"sqlite+pysqlite:///{credentials}", future=True, echo=True
            ),
        }

    def setup_sqlite(self, credentials=None, db_path="app.db"):
        return {
            "write": create_async_engine(
                f"sqlite+aiosqlite:///{db_path}", echo=False, future=True
            ),
            "read": create_async_engine(
                f"sqlite+aiosqlite:///{db_path}", echo=False, future=True
            ),
        }

    def create_postgres_database_if_not_exist(
        cls,
        database_url: str,
        default_database: str = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_DATABASE_DEFAULT}",
    ):
        engine = create_engine(default_database)
        db_name = database_url.split("/")[-1]
        conn = engine.connect()

        try:
            conn.execute(text("commit"))
            db_exists = conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
            ).scalar()

            if not db_exists:
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"Database {db_name} created successfully.")
            else:
                print(f"Database {db_name} already exists.")
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    async def create_all_tables(self):
        engine: AsyncEngine = self.engine["write"]

        async with engine.begin() as conn:
            await conn.run_sync(self._base.metadata.create_all)

    async def drop_all_tables(self):
        engine: AsyncEngine = self.engine["write"]
        async with engine.begin() as conn:
            await conn.run_sync(self._base.metadata.drop_all)
