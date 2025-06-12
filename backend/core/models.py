from datetime import datetime
from typing import Optional

from pendulum import now
from sqlmodel import Field, SQLModel


class BasePetfinderModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    petfinder_id: str = Field(index=True, unique=True)
    last_updated: datetime = Field(default_factory=now)

    model_config = {
        "arbitrary_types_allowed": True,
    }
