from pydantic import BaseModel, EmailStr
from typing import Optional


class ShelterCreate(BaseModel):
    petfinder_id: str
    name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
