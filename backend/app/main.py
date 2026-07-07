from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from spark.manager import SparkManagerService
from scheduler.scheduler import start_scheduler

from app.routers.lakehouse import router
from app.routers import etl
from app.routers import copilot


@asynccontextmanager
async def lifespan(app: FastAPI):

    # --------------------------------------------------
    # Runs when FastAPI starts
    # --------------------------------------------------

    print("Starting Health Scheduler...")
    start_scheduler()

    yield

    # --------------------------------------------------
    # Runs when FastAPI shuts down
    # --------------------------------------------------

    print("Stopping Spark Session...")
    SparkManagerService.stop()


app = FastAPI(
    title="Lakehouse Maintenance Copilot",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(etl.router)
app.include_router(copilot.router)