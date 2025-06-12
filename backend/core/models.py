# shared/models.py

from typing import Optional
from sqlmodel import SQLModel, Field
from pendulum import now, DateTime


class BasePetfinderModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    petfinder_id: str = Field(index=True, unique=True)
    last_updated: DateTime = Field(default_factory=now)

    model_config = {"arbitrary_types_allowed": True}
