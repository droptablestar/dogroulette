import os
import time

import httpx
from dotenv import load_dotenv

load_dotenv()


class PetfinderService:
    PETFINDER_CLIENT_ID = os.getenv("PETFINDER_CLIENT_ID")
    PETFINDER_CLIENT_SECRET = os.getenv("PETFINDER_CLIENT_SECRET")
    PETFINDER_TOKEN = None
    PETFINDER_TOKEN_EXPIRY = 0  # UNIX timestamp

    @classmethod
    async def get_petfinder_token(cls):
        global PETFINDER_TOKEN, PETFINDER_TOKEN_EXPIRY

        now = time.time()
        print("token:", cls.PETFINDER_TOKEN, cls.PETFINDER_TOKEN_EXPIRY)
        if cls.PETFINDER_TOKEN and now < cls.PETFINDER_TOKEN_EXPIRY:
            return cls.PETFINDER_TOKEN  # naive in-memory cache

        url = "https://api.petfinder.com/v2/oauth2/token"
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
