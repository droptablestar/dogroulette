import os
import time
from pprint import pprint
from typing import Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="DogRoulette API")

# Allow your frontend (localhost:3000 during dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PETFINDER_CLIENT_ID = os.getenv("PETFINDER_CLIENT_ID")
PETFINDER_CLIENT_SECRET = os.getenv("PETFINDER_CLIENT_SECRET")
PETFINDER_TOKEN = None
PETFINDER_TOKEN_EXPIRY = 0  # UNIX timestamp


async def get_petfinder_token():
    global PETFINDER_TOKEN, PETFINDER_TOKEN_EXPIRY

    now = time.time()
    if PETFINDER_TOKEN and now < PETFINDER_TOKEN_EXPIRY:
        return PETFINDER_TOKEN  # naive in-memory cache

    url = "https://api.petfinder.com/v2/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": PETFINDER_CLIENT_ID,
        "client_secret": PETFINDER_CLIENT_SECRET,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data)
        response.raise_for_status()

        json = response.json()
        PETFINDER_TOKEN = json["access_token"]
        PETFINDER_TOKEN_EXPIRY = now + json["expires_in"] - 60  # subtract buffer (60s)
        return PETFINDER_TOKEN


@app.get("/dogs")
async def get_dogs(
    limit: int = 1,
    location: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
):
    """
    Returns a list of adoptable dogs.
    Supports limiting results and optional location-based filtering.
    """
    token = await get_petfinder_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "type": "dog",
        "limit": limit,
    }
    if lat and lon:
        params["location"] = f"{lat},{lon}"
    elif location:
        params["location"] = location
    else:
        params["location"] = "10001"  # fallback zip

    async with httpx.AsyncClient() as client:
        res = await client.get(
            "https://api.petfinder.com/v2/animals", headers=headers, params=params
        )
        res.raise_for_status()
        data = res.json()["animals"]

    # Map Petfinder data to your Dog object shape
    dogs = []
    for animal in data:
        pprint(animal)
        address = animal.get("contact", {}).get("address", {})
        dog = {
            "id": animal.get("id"),
            "name": animal.get("name"),
            "breed": animal.get("breeds", {}).get("primary"),
            "location": f"{address.get('city')}, {address.get('state')}",
            "distance": animal.get("distance"),
            "age": animal.get("age"),
            "img_url": (
                animal["photos"][0]["medium"]
                if animal.get("photos")
                else "https://place-puppy.com/300x300"
            ),
            "source_url": animal["url"],
        }
        dogs.append(dog)

    return dogs
