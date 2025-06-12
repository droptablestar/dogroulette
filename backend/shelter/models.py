from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Relationship

from backend.core.models import BasePetfinderModel

if TYPE_CHECKING:
    from backend.pet.models import Pet


class Shelter(BasePetfinderModel, table=True):
    name: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    email: Optional[str]
    phone: Optional[str]

    pets: List["Pet"] = Relationship(back_populates="shelter")
