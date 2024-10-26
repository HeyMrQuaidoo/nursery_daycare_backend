import uvicorn
from fastapi import FastAPI

# local imports
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.routes import configure_routes
from app.core.middleware import configure_middleware

app = FastAPI(title=settings.APP_NAME, description="", lifespan=lifespan)

# configure middleware and routes
configure_middleware(app)
configure_routes(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.APP_URL, port=8002)
