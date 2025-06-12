from pprint import pprint
from typing import Optional

import httpx
from fastapi import APIRouter
from fastapi import Query

from backend.core.services import PetfinderService

router = APIRouter()


@router.get("/dogs")
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
    token = await PetfinderService.get_petfinder_token()
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
