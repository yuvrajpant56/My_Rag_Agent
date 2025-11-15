from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str
    ANTHROPIC_MODEL: str
    QDRANT_URL: str
    QDRANT_COLLECTION_NAME: str
    EMBEDDING_MODEL: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()