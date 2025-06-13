from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from backend.db.session import get_session

from .models import Shelter
from .repositories import create_shelter, list_shelters
from .schemas import ShelterCreate

router = APIRouter()


@router.post("/", response_model=Shelter)
def create_shelter_route(payload: ShelterCreate, session: Session = Depends(get_session)):
    try:
        return create_shelter(session, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/", response_model=list[Shelter])
def list_shelters_route(session: Session = Depends(get_session)):
    return list_shelters(session)
