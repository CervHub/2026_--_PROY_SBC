from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    tmp_dir: str = "outputs"
    output_dir: str = "outputs"
    debug: bool = False


    class Config:
        env_file = ".env"

settings = Settings()