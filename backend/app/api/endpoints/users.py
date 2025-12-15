from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from passlib.context import CryptContext
import uuid as uuid_pkg

from app.db.database import get_session
from app.models.user import User
from app.models.organization import Organization
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse
)

router = APIRouter(prefix="/users", tags=["Users"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
        user_data: UserCreate,
        session: Session = Depends(get_session)
):
    """
    Create a new user
    """
    # Verify organization exists
    org = session.get(Organization, user_data.org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {user_data.org_id} not found"
        )

    # Check if email already exists
    existing_email = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "email_already_exists",
                "message": f"User with email {user_data.email} already exists"
            }
        )

    # Create user with hashed password
    user_dict = user_data.model_dump(exclude={"password"})
    user_dict["password_hash"] = hash_password(user_data.password)
    user_dict["role"] = user_data.role.value  # Convert enum to string

    user = User(**user_dict)
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get("/", response_model=List[UserResponse])
async def get_users(
        skip: int = 0,
        limit: int = 100,
        org_id: uuid_pkg.UUID = None,
        is_active: bool = None,
        session: Session = Depends(get_session)
):
    """
    Get all users with optional filtering
    """
    query = select(User)

    if org_id is not None:
        query = query.where(User.org_id == org_id)

    if is_active is not None:
        query = query.where(User.is_active == is_active)

    query = query.offset(skip).limit(limit)
    users = session.exec(query).all()

    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
        user_id: uuid_pkg.UUID,
        session: Session = Depends(get_session)
):
    """
    Get user by ID
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    return user


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
        user_id: uuid_pkg.UUID,
        user_data: UserUpdate,
        session: Session = Depends(get_session)
):
    """
    Update user details
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    # Update fields
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "role" and value:
            setattr(user, key, value.value)  # Convert enum to string
        else:
            setattr(user, key, value)

    from datetime import datetime
    user.updated_at = datetime.utcnow()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: uuid_pkg.UUID,
        session: Session = Depends(get_session)
):
    """
    Soft delete user (set is_active to False)
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    user.is_active = False
    from datetime import datetime
    user.updated_at = datetime.utcnow()

    session.add(user)
    session.commit()

    return None
