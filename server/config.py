from pydantic import BaseSettings

class Settings(BaseSettings):
    postgres_host:str
    postgres_port:str
    postgres_user:str
    postgres_password:str
    postgres_db:str
    mail:str
    storage:str="./storage"
    static_web:str="client/public/"
    fixed_root:bool=False
    
    class Config:
        env_file = ".env"