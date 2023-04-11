from .models import db
from .config import Settings
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

settings=Settings()

config={
    "connections":{
        "default":{
            "engine":"tortoise.backends.asyncpg",
            "credentials":{
                "host":settings.postgres_host,
                "port":settings.postgres_port,
                "user":settings.postgres_user,
                "password":settings.postgres_password,
                "database":settings.postgres_db
            }
        }
    },
    "apps":{
        "models": {
            "models":[db, 'aerich.models'],
            'default_connection': 'default'
        }
    }
}

def register_db(app:FastAPI):
    register_tortoise(app=app, config=config, add_exception_handlers=True)