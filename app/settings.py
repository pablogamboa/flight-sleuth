from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bounds: str = "41.88,41.43,-1.31,-0.41"


settings = Settings()
