from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.auth.routes import router as auth_router
from backend.core.scheduler import start_scheduler
from backend.core.services import LoggingService
from backend.pet.routes import router as pet_router
from backend.shelter.routes import router as shelter_router

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    LoggingService.setup_logging()
    logger.warning("Starting scheduler...")
    start_scheduler()
    yield
    logger.error("Shutting down app...")


app = FastAPI(title="DogRoulette API", lifespan=lifespan)

app.include_router(auth_router, prefix="", tags=["Auth"])
app.include_router(pet_router, prefix="/pets", tags=["Pets"])
app.include_router(shelter_router, prefix="/shelters", tags=["Shelters"])

# Allow your frontend (localhost:3000 during dev)
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
