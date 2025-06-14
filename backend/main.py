from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import db  # noqa: F401
from core.scheduler import start_scheduler
from pet.routes import router as pet_router
from shelter.routes import router as shelter_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield


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
