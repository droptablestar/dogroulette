from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import JSON
from sqlmodel import Column, Field, Relationship

from backend.core.models import BasePetfinderModel

if TYPE_CHECKING:
    from backend.shelter.models import Shelter


class Pet(BasePetfinderModel, table=True):
    name: str
    age: Optional[str]
    gender: Optional[str]
    size: Optional[str]
    breed: Optional[str]
    description: Optional[str]
    photos: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    status: Optional[str]
    published_at: Optional[datetime] = Field(default=None)

    shelter_id: Optional[int] = Field(default=None, foreign_key="shelter.id")
    shelter: Optional["Shelter"] = Relationship(back_populates="pets")
