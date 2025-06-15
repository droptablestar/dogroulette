from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
