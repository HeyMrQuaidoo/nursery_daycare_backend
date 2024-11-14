from fastapi import FastAPI
from dogpile.cache import make_region
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logger import AppLogger
from app.db.dbManager import DBManager

# cache
from app.cache.cacheManager import CacheManager

# TODO (DQ) Add factory information
# Issue: https://github.com/compylertech/hskee-hsm-backend/issues/2
# - from app.factory.dataSeeder
# - from app.factory.dataFactory

# logger
logger = AppLogger().get_logger()

# get DB Info
db_manager = DBManager()
get_db = db_manager.db_module.get_db

cache_manager = CacheManager()

# create cache
cache_region = make_region().configure(
    "dogpile.cache.dbm",
    expiration_time=300,
    arguments={"filename": f"{settings.CACHE_PATH}cachefile.dbm"},
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup setup items
    global logger
    logger.info("Starting up")

    if not logger:
        app_logger = AppLogger()
        logger = app_logger.get_logger()

    # instantiate db
    await db_manager.db_module.create_all_tables()

    # cache
    cache_manager.get_instance()
    await cache_manager._initialize_cache_module()

    yield

    logger.info("Shutting down")
