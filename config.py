from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
	APP_NAME: str = "StrataTrade"
	DEBUG: bool = False
	
	model_config = SettingsConfigDict(env_file=".env",
		extra="ignore",
		)
settings = Settings()