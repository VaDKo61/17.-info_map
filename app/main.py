import uvicorn
from api import router as api_router
from core.config import settings
from core.security import verify_api_key
from fastapi import Depends, FastAPI

app = FastAPI(dependencies=[Depends(verify_api_key)])

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
