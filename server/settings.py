from pydantic_settings import BaseSettings

from utility import singleton


@singleton
class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: str = '5432'
    DB_NAME: str = 'dbname'
    DB_USER: str = 'username'
    DB_PASSWORD: str = 'password'

    def get_db_connection(self):
        return f'postgres://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
