import logging
from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.scheduler import start_scheduler
from backend.pet.routes import router as pet_router
from backend.shelter.routes import router as shelter_router

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting scheduler...")
    start_scheduler()
    yield
    logger.info("Shutting down app...")


app = FastAPI(title="DogRoulette API", lifespan=lifespan)

app.include_router(shelter_router, prefix="/shelters", tags=["Shelters"])
app.include_router(pet_router, prefix="/pets", tags=["Pets"])

# Allow your frontend (localhost:3000 during dev)
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
