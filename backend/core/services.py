import logging
import os
import sys
import time
from pprint import pprint

import colorlog
import httpx
import pendulum
from dotenv import load_dotenv
from sqlmodel import Session, select

from backend.db.session import get_session
from backend.pet.models import Pet

load_dotenv()

logger = logging.getLogger(__name__)


class PetfinderService:
    PETFINDER_CLIENT_ID = os.getenv("PETFINDER_CLIENT_ID")
    PETFINDER_CLIENT_SECRET = os.getenv("PETFINDER_CLIENT_SECRET")
    PETFINDER_TOKEN = None
    PETFINDER_TOKEN_EXPIRY = 0  # UNIX timestamp
    PETFINDER_URL = "https://api.petfinder.com/v2"

    @classmethod
    async def get_petfinder_token(cls):
        now = time.time()
        logger.info("token:", cls.PETFINDER_TOKEN, cls.PETFINDER_TOKEN_EXPIRY)
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
        # Upsert pet
        petfinder_id = data.get("id", 0)
        logger.info(f"petfinder id: {petfinder_id}")
        pet = session.exec(select(Pet).where(Pet.petfinder_id == petfinder_id)).first()
        if not pet:
            pet = Pet(
                petfinder_id=petfinder_id,
                name=data.get("name"),
                age=data.get("age"),
                gender=data.get("gender"),
                size=data.get("size"),
                breed=data.get("breeds", {}).get("primary"),
                description=data.get("description"),
                photos=data.get("photos"),
                status=data.get("status"),
                published_at=data.get("published_at"),
                last_updated=pendulum.now("UTC"),
            )
            session.add(pet)

        session.commit()

    @classmethod
    async def run_sync(cls):
        locations = ["Baltimore, MD"]
        for location in locations:
            await cls.sync_data(location)

    @classmethod
    async def sync_data(cls, location: str | tuple[float, float] | int):
        """
        This method is intended to run periodically and keep local DB data in
        sync with Petfinder (and/or any other APIs we integrate with in the
        future).

        Args:
            location: city, state; latitude,longitude; or postal code.
        Returns:
            `None`
        """
        token = await cls.get_petfinder_token()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"{cls.PETFINDER_URL}/animals"
        limit = 1000
        page = 1
        page_limit = 1
        logger.info(f"Running sync on {location}...")
        logger.info(f"headers: {headers}")
        logger.info(f"url: {url}")
        pets = []
        while page <= page_limit and page < 50:
            logger.info(f"Reqesting page {page}...")
            async with httpx.AsyncClient() as client:
                try:
                    res = await client.get(
                        f"{cls.PETFINDER_URL}/animals",
                        headers=headers,
                        params={
                            "type": "dog",
                            "location": location,
                            "limit": min(limit, 100),  # fix here
                            "page": page,
                        },
                    )
                    res.raise_for_status()
                except httpx.HTTPStatusError as exc:
                    print(
                        f"Petfinder API error {exc.response.status_code}: {exc.response.text}"
                    )
                    continue
            data = res.json()
            pprint(data)
            pets.extend(data["animals"])

            # check pagination for more results
            pagination = data.get("pagination", {})
            page = pagination.get("current_page", page) + 1
            page_limit = pagination.get("total_pages", page)
            if page > page_limit:
                time.sleep(0.5)
            logger.info("")
            logger.info("*" * 50)
            logger.info("")
            pprint(pets[0])
            logger.info("*" * 50)

            with next(get_session()) as session:
                for pet_data in pets:
                    cls.store_data(pet_data, session)


class LoggingService:
    @staticmethod
    def setup_logging():
        handler = colorlog.StreamHandler(sys.stdout)
        handler.setFormatter(
            colorlog.ColoredFormatter(
                "%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            )
        )
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.handlers.clear()  # This line removes any default handlers
        root_logger.addHandler(handler)

        # Now explicitly quiet third-party loggers
        for noisy in ("httpx", "sqlalchemy.engine"):
            lgr = logging.getLogger(noisy)
            lgr.setLevel(logging.WARNING)
            lgr.handlers.clear()

        logging.basicConfig(level=logging.INFO, handlers=[handler])

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)
