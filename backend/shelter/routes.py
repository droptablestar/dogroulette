from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from backend.db.session import get_session
from .schemas import ShelterCreate
from .models import Shelter
from .repositories import create_shelter

router = APIRouter()


@router.post("/", response_model=Shelter)
def create_shelter_route(
    payload: ShelterCreate, session: Session = Depends(get_session)
):
    try:
        return create_shelter(session, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
