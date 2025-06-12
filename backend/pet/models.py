from typing import Optional

from pendulum import DateTime, now
from sqlmodel import Field, Relationship
from typing_extensions import TYPE_CHECKING

from backend.core.models import BasePetfinderModel

if TYPE_CHECKING:
    from backend.shelter.models import Shelter


class Pet(BasePetfinderModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    petfinder_id: str = Field(index=True, unique=True)
    name: str
    age: Optional[str]
    gender: Optional[str]
    size: Optional[str]
    breed: Optional[str]
    description: Optional[str]
    photos: Optional[dict]
    status: Optional[str]
    published_at: Optional[DateTime]
    last_updated: DateTime = Field(default_factory=now)

    shelter_id: Optional[int] = Field(default=None, foreign_key="shelter.id")
    shelter: Optional["Shelter"] = Relationship(back_populates="pets")
