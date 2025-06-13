from sqlmodel import Relationship

from backend.pet.models import Pet
from backend.shelter.models import Shelter

Pet.shelter = Relationship(back_populates="pets")
Shelter.pets = Relationship(back_populates="shelter")

Pet.model_rebuild()
Shelter.model_rebuild()

__all__ = ["session"]
