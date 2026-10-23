from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parent/"user_service.env"

class Settings(BaseSettings):
	DATABASE_URL : str
	JWT_SECRET_KEY : str 
	JWT_ALGORITHM : str = "HS256"
	ACCESS_TOKEN_EXPIRE_MINUTES : int = 15
	COOKIE_SECURE : bool = False

	model_config=SettingsConfigDict(env_file=ENV_FILE,extra="ignore")

settings = Settings()