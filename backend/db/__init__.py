from sqlmodel import Relationship

from backend.auth.models import User
from backend.pet.models import Pet
from backend.shelter.models import Shelter

Pet.shelter = Relationship(back_populates="pets")
Shelter.pets = Relationship(back_populates="shelter")

User.model_rebuild()
Pet.model_rebuild()
Shelter.model_rebuild()

__all__ = ["session"]
