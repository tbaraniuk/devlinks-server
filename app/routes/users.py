from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlmodel import select
# from pydrive2.auth import GoogleAuth
# from pydrive2.drive import GoogleDrive

from database import SessionDep
from schemas.user import UserGet, UserSchema, UserUpdate
from models.user import User
from auth.utils import get_current_user
from config import Settings


# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()

# drive = GoogleDrive(gauth)


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get('/me/')
def get_user_self_info(user: UserSchema = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "links": user.links
    }


@router.get('/{username}/', response_model=UserGet)
def get_user_profile(username: str, session: SessionDep):
    db_user = session.exec(select(User).where(User.username == username)).first()

    return db_user


# @router.post('/upload-avatar/')
# def upload_user_avatar(session: SessionDep, file: UploadFile = File(...), user: UserSchema = Depends(get_current_auth_user)):
#     files = {
#         "file": (file.filename, file.file, file.content_type),
#     }

#     try:
#         drive_file = drive.CreateFile({'title': file.filename})
#         drive_file.SetContentFile(file)
#         drive_file.Upload()
#         print(drive_file)
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put('/update-user/', response_model=UserGet, status_code=status.HTTP_200_OK)
def update_user(user_update: UserUpdate, session: SessionDep, user: UserSchema = Depends(get_current_user)):
    user.first_name = user_update.first_name
    user.last_name = user_update.last_name
    user.email = user_update.email

    session.add(user)
    session.commit()
    session.refresh(user)
    return user