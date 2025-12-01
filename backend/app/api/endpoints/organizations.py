from time import sleep

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import uuid as uuid_pkg

from app.db.database import get_session
from app.models.organization import Organization
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse
)

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
        org_data: OrganizationCreate,
        session: Session = Depends(get_session)
):
    """
    Create a new organization
    """
    # Only check if email already exists
    existing_email = session.exec(
        select(Organization).where(Organization.primary_email == org_data.primary_email)
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "email_already_exists",
                "message": f"Organization with email {org_data.primary_email} already exists",
                "field": "primary_email"
            }
        )

    # Create organization
    organization = Organization(**org_data.model_dump())
    session.add(organization)
    session.commit()
    session.refresh(organization)

    return organization


@router.get("/", response_model=List[OrganizationResponse])
async def get_organizations(
        skip: int = 0,
        limit: int = 100,
        is_active: bool = None,
        session: Session = Depends(get_session)
):
    """
    Get all organizations with optional filtering
    """
    query = select(Organization)

    if is_active is not None:
        query = query.where(Organization.is_active == is_active)

    query = query.offset(skip).limit(limit)
    organizations = session.exec(query).all()

    return organizations


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
        org_id: uuid_pkg.UUID,
        session: Session = Depends(get_session)
):
    """
    Get organization by ID
    """
    organization = session.get(Organization, org_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {org_id} not found"
        )

    return organization


@router.get("/code/{code}", response_model=OrganizationResponse)
async def get_organization_by_code(
        code: str,
        session: Session = Depends(get_session)
):
    """
    Get organization by 5-digit code
    """
    organization = session.exec(
        select(Organization).where(Organization.code == code)
    ).first()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with code {code} not found"
        )

    return organization


@router.patch("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
        org_id: uuid_pkg.UUID,
        org_data: OrganizationUpdate,
        session: Session = Depends(get_session)
):
    """
    Update organization details
    """
    organization = session.get(Organization, org_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {org_id} not found"
        )

    # Update fields
    update_data = org_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(organization, key, value)

    from datetime import datetime
    organization.updated_at = datetime.utcnow()

    session.add(organization)
    session.commit()
    session.refresh(organization)

    return organization


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
        org_id: uuid_pkg.UUID,
        session: Session = Depends(get_session)
):
    """
    Soft delete organization (set is_active to False)
    """
    organization = session.get(Organization, org_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {org_id} not found"
        )

    organization.is_active = False
    from datetime import datetime
    organization.updated_at = datetime.utcnow()

    session.add(organization)
    session.commit()

    return None
