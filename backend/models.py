from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class Shelter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    petfinder_id: str = Field(index=True, unique=True)
    name: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    pets: List["Pet"] = Relationship(back_populates="shelter")


class Pet(SQLModel, table=True):
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
    published_at: Optional[datetime]
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    shelter_id: Optional[int] = Field(default=None, foreign_key="shelter.id")
    shelter: Optional[Shelter] = Relationship(back_populates="pets")
