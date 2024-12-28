import logging
import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from typing import ClassVar
from oauth2client.client import OAuth2Credentials


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


load_dotenv(dotenv_path='../.env')
BASE_DIR = Path(__file__).parent


UPLOAD_DIR = "uploaded_images"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


class DbSettings(BaseModel):
    url: str = os.getenv('DATABASE_URL')
    echo: bool = True


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class GoogleDriveAuth(BaseModel):
    gauth: ClassVar[GoogleAuth] = GoogleAuth()
    gauth.credentials = OAuth2Credentials(
        token_uri=os.getenv("GOOGLE_REDIRECT_TOKEN"),
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        refresh_token=os.getenv("GOOGLE_REFRESH_TOKEN"),
        access_token=os.getenv("GOOGLE_ACCESS_TOKEN"),
        token_expiry=None,
        user_agent=None,
        revoke_uri=None,
    )
    try:
        print("Initializing Google Drive...")
        drive: ClassVar[GoogleDrive] = GoogleDrive(gauth)
        print("Google Drive initialized successfully!")
    except Exception as e:
        print(f"Error initializing Google Drive: {e}")


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    db: DbSettings = DbSettings()
    google_drive: GoogleDriveAuth = GoogleDriveAuth()


settings = Settings()
