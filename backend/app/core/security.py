from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings
password_hash = PasswordHash.recommended()




def create_access_token(user_id: int) -> str:
    """Create a signed JWT access token for a user."""

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=30),
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm="HS256",
    )
def hash_password(password: str) -> str:
    """Hash a password before storing it in the database."""
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Check a password against its stored hash."""
    return password_hash.verify(plain_password, hashed_password)