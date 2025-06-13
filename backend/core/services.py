import asyncio
import os
import time
from datetime import datetime

import httpx
from dotenv import load_dotenv
from sqlmodel import Session, select

from backend.db.session import get_session
from backend.pet.models import Pet
from backend.shelter.models import Shelter

load_dotenv()


class PetfinderService:
    PETFINDER_CLIENT_ID = os.getenv("PETFINDER_CLIENT_ID")
    PETFINDER_CLIENT_SECRET = os.getenv("PETFINDER_CLIENT_SECRET")
    PETFINDER_TOKEN = None
    PETFINDER_TOKEN_EXPIRY = 0  # UNIX timestamp
    PETFINDER_URL = "https://api.petfinder.com/v2"

    @classmethod
    async def get_petfinder_token(cls):
        now = time.time()
        print("token:", cls.PETFINDER_TOKEN, cls.PETFINDER_TOKEN_EXPIRY)
        if cls.PETFINDER_TOKEN and now < cls.PETFINDER_TOKEN_EXPIRY:
            return cls.PETFINDER_TOKEN  # naive in-memory cache

        url = f"{cls.PETFINDER_URL}/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": cls.PETFINDER_CLIENT_ID,
            "client_secret": cls.PETFINDER_CLIENT_SECRET,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data)
            response.raise_for_status()

            json = response.json()
            cls.PETFINDER_TOKEN = json["access_token"]
            cls.PETFINDER_TOKEN_EXPIRY = now + json["expires_in"] - 60
            return cls.PETFINDER_TOKEN

    @staticmethod
    def store_data(data: dict, session: Session):
        # Upsert shelter
        shelter_info = data.get("organization", {})
        shelter = session.exec(
            select(Shelter).where(Shelter.petfinder_id == shelter_info["id"])
        ).first()
        if not shelter:
            shelter = Shelter(
                petfinder_id=shelter_info["id"],
                name=shelter_info.get("name"),
                city=shelter_info.get("address", {}).get("city"),
                state=shelter_info.get("address", {}).get("state"),
                country="US",  # fallback default
                email=shelter_info.get("email"),
                phone=shelter_info.get("phone"),
                last_updated=datetime.utcnow(),
            )
            session.add(shelter)
            session.flush()

        # Upsert pet
        petfinder_id = data["id"]
        pet = session.exec(select(Pet).where(Pet.petfinder_id == str(petfinder_id))).first()
        if not pet:
            pet = Pet(
                petfinder_id=str(petfinder_id),
                last_updated=datetime.utcnow(),
                name=data.get("name"),
                age=data.get("age"),
                gender=data.get("gender"),
                size=data.get("size"),
                breed=data.get("breeds", {}).get("primary"),
                description=data.get("description"),
                photos=data.get("photos"),
                status=data.get("status"),
                published_at=data.get("published_at"),
                shelter_id=shelter.id,
            )
            session.add(pet)

        session.commit()

    @classmethod
    async def run_sync(cls):
        headers = {"Authorization": f"Bearer {cls.PETFINDER_TOKEN}"}
        location = "10001"
        limit = 100

        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"{cls.PETFINDER_URL}/animals",
                headers=headers,
                params={"type": "dog", "location": location, "limit": limit},
            )
            res.raise_for_status()
            data = res.json()

        pets = data["animals"]

        with next(get_session()) as session:
            for pet_data in pets:
                cls.store_data(pet_data, session)

    if __name__ == "__main__":
        asyncio.run(run_sync())
