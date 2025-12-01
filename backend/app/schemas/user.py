from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserRole
import uuid as uuid_pkg


class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    role: UserRole = UserRole.STAFF


class UserCreate(UserBase):
    """Schema for creating user"""
    org_id: uuid_pkg.UUID
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """Schema for updating user"""
    full_name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user response (without password)"""
    id: uuid_pkg.UUID
    org_id: uuid_pkg.UUID
    is_active: bool
    is_logged_in: bool
    last_login_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str
