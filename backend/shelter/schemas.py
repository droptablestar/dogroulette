from pydantic import BaseModel, EmailStr


class ShelterCreate(BaseModel):
    petfinder_id: str
    name: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
