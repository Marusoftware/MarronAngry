from .models import db
from tortoise import Tortoise
from .config import Settings

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

async def init_db():
    await Tortoise.init(config=config)

async def final_db():
    await Tortoise.close_connections()