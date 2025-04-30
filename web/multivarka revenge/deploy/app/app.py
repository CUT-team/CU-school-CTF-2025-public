from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from app.api.endpoints import routers
from app.db.base import init_models
from app.db.models import Job
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    yield
    
app = FastAPI(title="CSV Analyzer with ClickHouse", lifespan=lifespan, root_path="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    logging.info(f"Including router: {router.prefix}")
    app.include_router(router)