from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "organization" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(1024) NOT NULL,
    "description" VARCHAR(2048) NOT NULL  DEFAULT ''
);;
        CREATE TABLE IF NOT EXISTS "project" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(1024) NOT NULL,
    "description" VARCHAR(2048) NOT NULL  DEFAULT '',
    "organization_id" UUID NOT NULL REFERENCES "organization" ("id") ON DELETE CASCADE
);;
        CREATE TABLE IF NOT EXISTS "task" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(1024) NOT NULL,
    "description" VARCHAR(2048) NOT NULL  DEFAULT '',
    "time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "project_id" UUID NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE
);;
        CREATE TABLE "organization_user" (
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "organization_id" UUID NOT NULL REFERENCES "organization" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "organization_user";
        DROP TABLE IF EXISTS "organization";
        DROP TABLE IF EXISTS "project";
        DROP TABLE IF EXISTS "task";"""
