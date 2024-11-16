import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from typing import Annotated, Optional, Union

from database import get_session
from config import settings
from models.user import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(get_session)]):
    print(token)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing from request",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_jwt(token)
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token payload missing 'username' field",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: Optional[timedelta] = None
    ):
    to_encode = payload.copy()
    now = datetime.utcnow()

    if expire_timedelta:
        expire = now + timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)

    return encoded


def decode_jwt(token: Union[str, bytes], public_key: str = settings.auth_jwt.public_key_path.read_text(), algorithm: str = settings.auth_jwt.algorithm):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])

    return decoded


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> bytes:
    return pwd_context.hash(plain_password)