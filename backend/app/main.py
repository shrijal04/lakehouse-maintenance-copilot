from fastapi import FastAPI

from app.routers.lakehouse import router

app = FastAPI(
    title="Lakehouse Maintenance Copilot"
)

app.include_router(router)