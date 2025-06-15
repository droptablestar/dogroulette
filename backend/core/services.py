import logging
import os
import time

import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class PetfinderService:
    PETFINDER_CLIENT_ID = os.getenv("PETFINDER_CLIENT_ID")
    PETFINDER_CLIENT_SECRET = os.getenv("PETFINDER_CLIENT_SECRET")
    PETFINDER_URL = "https://api.petfinder.com/v2"
    _petfinder_token = None
    _petfinder_token_expiry = 0  # UNIX timestamp

    @classmethod
    def get_petfinder_token(cls):
        now = time.time()
        logger.info("token:", cls._petfinder_token, cls._petfinder_token_expiry)
        if cls._petfinder_token and now < cls._petfinder_token_expiry:
            return cls._petfinder_token  # naive in-memory cache

        url = f"{cls.PETFINDER_URL}/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": cls.PETFINDER_CLIENT_ID,
            "client_secret": cls.PETFINDER_CLIENT_SECRET,
        }
        response = httpx.post(url, data=data)
        response.raise_for_status()

        json = response.json()
        cls._petfinder_token = json["access_token"]
        cls._petfinder_token_expiry = now + json["expires_in"] - 60
        return cls._petfinder_token

    #
    # @staticmethod
    # def store_data(data: dict, session: Session):
    #     # Upsert pet
    #     petfinder_id = data.get("id", 0)
    #     logger.info(f"petfinder id: {petfinder_id}")
    #     pet = session.exec(select(Pet).where(Pet.petfinder_id == petfinder_id)).first()
    #     if not pet:
    #         pet = Pet(
    #             petfinder_id=petfinder_id,
    #             name=data.get("name"),
    #             age=data.get("age"),
    #             gender=data.get("gender"),
    #             size=data.get("size"),
    #             breed=data.get("breeds", {}).get("primary"),
    #             description=data.get("description"),
    #             photos=data.get("photos"),
    #             status=data.get("status"),
    #             published_at=data.get("published_at"),
    #             last_updated=pendulum.now("UTC"),
    #         )
    #         session.add(pet)
    #
    #     session.commit()
    #
    # @classmethod
    # async def run_sync(cls):
    #     locations = ["Baltimore, MD"]
    #     for location in locations:
    #         await cls.sync_data(location)
    #
    # @classmethod
    # async def sync_data(cls, location: str | tuple[float, float] | int):
    #     """
    #     This method is intended to run periodically and keep local DB data in
    #     sync with Petfinder (and/or any other APIs we integrate with in the
    #     future).
    #
    #     Args:
    #         location: city, state; latitude,longitude; or postal code.
    #     Returns:
    #         `None`
    #     """
    #     token = await cls.get_petfinder_token()
    #     headers = {"Authorization": f"Bearer {token}"}
    #     url = f"{cls.PETFINDER_URL}/animals"
    #     limit = 1000
    #     page = 1
    #     page_limit = 1
    #     logger.info(f"Running sync on {location}...")
    #     logger.info(f"headers: {headers}")
    #     logger.info(f"url: {url}")
    #     pets = []
    #     while page <= page_limit and page < 50:
    #         logger.info(f"Reqesting page {page}...")
    #         async with httpx.AsyncClient() as client:
    #             try:
    #                 res = await client.get(
    #                     f"{cls.PETFINDER_URL}/animals",
    #                     headers=headers,
    #                     params={
    #                         "type": "dog",
    #                         "location": location,
    #                         "limit": min(limit, 100),  # fix here
    #                         "page": page,
    #                     },
    #                 )
    #                 res.raise_for_status()
    #             except httpx.HTTPStatusError as exc:
    #                 print(
    #                     f"Petfinder API error {exc.response.status_code}: {exc.response.text}"
    #                 )
    #                 continue
    #         data = res.json()
    #         pprint(data)
    #         pets.extend(data["animals"])
    #
    #         # check pagination for more results
    #         pagination = data.get("pagination", {})
    #         page = pagination.get("current_page", page) + 1
    #         page_limit = pagination.get("total_pages", page)
    #         if page > page_limit:
    #             time.sleep(0.5)
    #         logger.info("")
    #         logger.info("*" * 50)
    #         logger.info("")
    #         pprint(pets[0])
    #         logger.info("*" * 50)
    #
    #         with next(get_session()) as session:
    #             for pet_data in pets:
    #                 cls.store_data(pet_data, session)
