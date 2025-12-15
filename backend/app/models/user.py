from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid as uuid_pkg


class UserRole(str, Enum):
    """User role enumeration"""
    ADMIN = "admin"
    STAFF = "staff"


class User(SQLModel, table=True):
    """
    User model for admin, staff, and viewer accounts
    """
    __tablename__ = "users"

    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )
    org_id: uuid_pkg.UUID = Field(foreign_key="organizations.id", nullable=False, index=True)

    username: str = Field(max_length=100, unique=False, nullable=False, index=True)
    email: str = Field(max_length=255, unique=True, nullable=False, index=True)
    password_hash: str = Field(max_length=255, nullable=False)

    role: str = Field(default=UserRole.STAFF.value, max_length=20)

    is_active: bool = Field(default=True, index=True)
    is_logged_in: bool = Field(default=False)
    last_login_at: Optional[datetime] = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
