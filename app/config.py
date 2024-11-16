import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings


load_dotenv(dotenv_path='../.env')
BASE_DIR = Path(__file__).parent





class DbSettings(BaseModel):
    url: str = os.getenv('DATABASE_URL')
    echo: bool = True


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    db: DbSettings = DbSettings()


settings = Settings()
