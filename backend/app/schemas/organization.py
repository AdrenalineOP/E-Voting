from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import uuid as uuid_pkg


class OrganizationBase(BaseModel):
    """Base organization schema"""
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=5, max_length=8)
    primary_email: EmailStr


class OrganizationCreate(OrganizationBase):
    """Schema for creating organization"""
    pass


class OrganizationUpdate(BaseModel):
    """Schema for updating organization"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    is_active: Optional[bool] = None


class OrganizationResponse(OrganizationBase):
    """Schema for organization response"""
    id: uuid_pkg.UUID
    current_election_id: Optional[uuid_pkg.UUID]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
