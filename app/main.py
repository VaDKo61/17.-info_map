import uvicorn
from fastapi import FastAPI

from core.config import settings

app = FastAPI()
from fastapi import APIRouter

app.include_router(APIRouter(), prefix=settings.api.prefix)

if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.run.host, port=settings.run.port)
