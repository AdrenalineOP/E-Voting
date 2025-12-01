from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid as uuid_pkg


class Organization(SQLModel, table=True):
    """
    Organization/School model
    """
    __tablename__ = "organizations"

    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )
    name: str = Field(max_length=255, nullable=False)
    code: str = Field(max_length=5, nullable=False)
    primary_email: str = Field(max_length=255, unique=True, nullable=False, index=True)

    current_election_id: Optional[uuid_pkg.UUID] = Field(default=None)

    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

