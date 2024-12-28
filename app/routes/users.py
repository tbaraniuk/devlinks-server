import os
from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlmodel import select
from typing import Annotated, Optional
from pydantic import EmailStr

from database import SessionDep
from schemas.user import UserGet, UserSchema
from models.user import User
from auth.utils import get_current_user
from config import UPLOAD_DIR
from helpers import get_drive_file


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get('/me/', response_model=UserGet)
def get_user_self_info(user: UserSchema = Depends(get_current_user)):
    """
    Fetch details of the currently authenticated user.
    """
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "links": user.links,
        "avatar_id": user.avatar_id
    }


@router.get('/{username}/', response_model=UserGet)
def get_user_profile(username: str, session: SessionDep):
    """
    Fetch the profile of a user by their username.
    """
    db_user = session.exec(select(User).where(User.username == username)).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.put('/update-user/', response_model=UserGet, status_code=status.HTTP_200_OK)
def update_user(first_name: Annotated[str, Form()],
                last_name: Annotated[str, Form()],
                email: Annotated[EmailStr, Form()],
                session: SessionDep,
                user: UserSchema = Depends(get_current_user),
                file: Annotated[Optional[UploadFile], File(description='Optional file upload')] = None):
    """
    Update user profile details.
    """
    user.first_name = first_name
    user.last_name = last_name
    user.email = email

    if file:
        try:
            if not file.content_type.startswith("image/"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Uploaded file is not an image."
                )

            file_path = os.path.join(UPLOAD_DIR, file.filename)

            with open(file_path, "wb") as f:
                f.write(file.file.read())

            user.avatar_id = file.filename
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saving file: {str(e)}"
            )
        # try:
        #     with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        #         temp_file.write(file.file.read())
        #         temp_file_path = temp_file.name

        #     google_drive = settings.google_drive.drive
        #     drive_file = google_drive.CreateFile({'title': file.filename})
        #     drive_file.SetContentFile(temp_file_path)
        #     drive_file.Upload()

        #     user.avatar_id = drive_file['id']
        # except Exception as e:
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        # finally:
        #     if os.path.exists(temp_file_path):
        #         os.remove(temp_file_path)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# @router.get("/get-avatar/{file_id}")
# async def get_avatar_image(file_id: str):
#     try:
#         file_content, mime_type, file_name, file_size = get_drive_file(file_id)

#         return StreamingResponse(file_content, media_type=mime_type)

#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error: {str(e)}")