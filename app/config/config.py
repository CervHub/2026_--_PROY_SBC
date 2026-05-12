from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    output_dir: str = "outputs"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()