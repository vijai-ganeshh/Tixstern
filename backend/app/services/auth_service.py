from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import UserRegister


async def register_user(
    db: AsyncSession,
    user_data: UserRegister,
) -> User:
    """Register a new user in the database."""

    # 1. Check whether the email already exists.
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_email = result.scalar_one_or_none()

    if existing_email:
        raise ValueError("Email is already registered.")

    # 2. Check whether the username is already taken.
    result = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    existing_username = result.scalar_one_or_none()

    if existing_username:
        raise ValueError("Username is already taken.")

    # 3. Hash the password and create the user.
    new_user = User(
        username=user_data.username,
        email=str(user_data.email),
        hashed_password=hash_password(user_data.password),
    )

    db.add(new_user)

    # 4. Save the user to PostgreSQL.
    try:
        await db.commit()
        await db.refresh(new_user)
    except Exception:
        await db.rollback()
        raise

    return new_user
  
async def login_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> tuple[User, str]:
    """Authenticate a user and return the user with an access token."""

    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if user is None or not verify_password(
        password, user.hashed_password
    ):
        raise ValueError("Invalid email or password.")

    if not user.is_active:
        raise ValueError("This account is inactive.")

    access_token = create_access_token(user.id)

    return user, access_token