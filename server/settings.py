from pydantic_settings import BaseSettings

from server.utility import singleton


@singleton
class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "dbname"
    DB_USER: str = "username"
    DB_PASSWORD: str = "password"

    def get_connection(self):
        return (
            f"postgres://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
