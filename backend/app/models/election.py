from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid as uuid_pkg
from enum import Enum

class ElectionStatus(str, Enum):
    """Election status enumeration"""
    UPCOMING= "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Election(SQLModel, table=True):
    """
    User model for admin, staff, and viewer accounts
    """
    __tablename__ = "elections"

    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )
    org_id: uuid_pkg.UUID = Field(foreign_key="organizations.id", nullable=False, index=True)
    created_by: uuid_pkg.UUID = Field(foreign_key="users.id", nullable=False, index=True)

    name: str = Field(max_length=100, unique=False, nullable=False, index=True)
    description: Optional[str] = Field(default=None, max_length=500)
    status: str = Field(default= ElectionStatus.UPCOMING, max_length=20)
    allow_anonymous_voting: bool = Field(default=False, index=True)
    
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
