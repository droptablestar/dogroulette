from typing import List, Optional

from sqlmodel import Session, select
from .models import Shelter
from .schemas import ShelterCreate
import pendulum


def create_shelter(session: Session, data: ShelterCreate) -> Shelter:
    stmt = select(Shelter).where(Shelter.petfinder_id == data.petfinder_id)
    existing = session.exec(stmt).first()

    if existing:
        raise ValueError("Shelter already exists")

    shelter = Shelter(**data.model_dump(), last_updated=pendulum.now())
    session.add(shelter)
    session.commit()
    session.refresh(shelter)
    return shelter


def list_shelters(session: Session) -> List[Shelter]:
    return list(session.exec(select(Shelter)).all())
