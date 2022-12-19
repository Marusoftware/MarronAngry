from .models import db
from tortoise import Tortoise
from .config import Settings

settings=Settings()

async def init_db():
    await Tortoise.init({
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
                "models":[db],
                'default_connection': 'default'
            }
        }
    })
    await Tortoise.generate_schemas(safe=True)

async def final_db():
    await Tortoise.close_connections()