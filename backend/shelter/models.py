from typing import TYPE_CHECKING

from sqlmodel import Relationship

from backend.core.models import BasePetfinderModel

if TYPE_CHECKING:
    from backend.pet.models import Pet


class Shelter(BasePetfinderModel, table=True):
    name: str | None
    city: str | None
    state: str | None
    country: str | None
    email: str | None
    phone: str | None

    pets: list["Pet"] = Relationship(back_populates="shelter")
