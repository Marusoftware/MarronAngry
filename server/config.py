from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):
    postgres_host:str
    postgres_port:str
    postgres_user:str
    postgres_password:str
    postgres_db:str