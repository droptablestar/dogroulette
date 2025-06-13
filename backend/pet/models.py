from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON
from sqlmodel import Column, Field, Relationship

from backend.core.models import BasePetfinderModel

if TYPE_CHECKING:
    from backend.shelter.models import Shelter


class Pet(BasePetfinderModel, table=True):
    name: str
    age: str | None
    gender: str | None
    size: str | None
    breed: str | None
    description: str | None
    photos: dict | None = Field(default=None, sa_column=Column(JSON))
    status: str | None
    published_at: datetime | None = Field(default=None)

    shelter_id: int | None = Field(default=None, foreign_key="shelter.id")
    shelter: Optional["Shelter"] = Relationship(back_populates="pets")
