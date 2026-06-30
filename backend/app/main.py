from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from spark.manager import spark
from app.routers.lakehouse import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs when FastAPI starts
    yield

    # Runs when FastAPI shuts down
    print("Stopping Spark Session...")
    spark.stop()


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