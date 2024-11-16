from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlmodel import select
from typing import Annotated

from auth.utils import hash_password, encode_jwt, verify_password
from schemas.token import Token
from schemas.user import UserSchema, RegisterGetUserSchema, UserCreate
from models.user import User
from database import SessionDep


router = APIRouter(prefix="/auth", tags=["Auth"])


def validate_auth_user(
        username: Annotated[str, Form()],
        password: Annotated[str, Form()],
        session: SessionDep
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
    )

    user = session.exec(select(User).where(User.username == username)).first()

    if not user:
        raise unauthed_exc

    if not verify_password(plain_password=password, hashed_password=user.password):
        raise unauthed_exc

    return user


@router.post('/register/', response_model=RegisterGetUserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: SessionDep):
    """
    Register user
    """
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already registered")

    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, username=user.username, password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    jwt_payload = {
        "id": str(new_user.id),
        "username": new_user.username
    }
    token = encode_jwt(jwt_payload)

    return {"user": new_user, "token":  Token(
        access_token=token,
        token_type="Bearer"
    )}


@router.post("/login/", response_model=Token)
def auth_user(user: UserSchema = Depends(validate_auth_user)):
    """
    Login user
    """
    jwt_payload = {
        "id": str(user.id),
        "username": user.username
    }
    token = encode_jwt(jwt_payload)
    return Token(
        access_token=token,
        token_type="Bearer"
    )
