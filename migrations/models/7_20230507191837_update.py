from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "organization" ADD "logo" UUID;
        ALTER TABLE "project" ADD "default_storage" UUID;
        ALTER TABLE "task" ADD "start" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "task" RENAME COLUMN "time" TO "end";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "task" RENAME COLUMN "end" TO "time";
        ALTER TABLE "task" DROP COLUMN "start";
        ALTER TABLE "project" DROP COLUMN "default_storage";
        ALTER TABLE "organization" DROP COLUMN "logo";"""
