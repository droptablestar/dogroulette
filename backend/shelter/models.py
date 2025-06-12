from typing import List, Optional, TYPE_CHECKING

from pendulum import DateTime, now
from sqlmodel import Field, Relationship

from backend.core.models import BasePetfinderModel

if TYPE_CHECKING:
    from backend.pet.models import Pet


class Shelter(BasePetfinderModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    petfinder_id: str = Field(index=True, unique=True)
    name: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    last_updated: DateTime = Field(default_factory=now)

    pets: List["Pet"] = Relationship(back_populates="shelter")
