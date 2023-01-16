from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "organization" ALTER COLUMN "name" TYPE VARCHAR(1024) USING "name"::VARCHAR(1024);
        ALTER TABLE "organization" ALTER COLUMN "description" TYPE VARCHAR(2048) USING "description"::VARCHAR(2048);
        ALTER TABLE "organizationmember" ALTER COLUMN "is_admin" TYPE BOOL USING "is_admin"::BOOL;
        ALTER TABLE "project" ALTER COLUMN "description" TYPE VARCHAR(2048) USING "description"::VARCHAR(2048);
        ALTER TABLE "project" ALTER COLUMN "name" TYPE VARCHAR(1024) USING "name"::VARCHAR(1024);
        ALTER TABLE "task" ALTER COLUMN "time" TYPE TIMESTAMPTZ USING "time"::TIMESTAMPTZ;
        ALTER TABLE "task" ALTER COLUMN "name" TYPE VARCHAR(1024) USING "name"::VARCHAR(1024);
        ALTER TABLE "task" ALTER COLUMN "description" TYPE VARCHAR(2048) USING "description"::VARCHAR(2048);
        ALTER TABLE "user" ADD "otp_recovery" VARCHAR(6);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "task" ALTER COLUMN "time" TYPE TIMESTAMPTZ USING "time"::TIMESTAMPTZ;
        ALTER TABLE "task" ALTER COLUMN "name" TYPE VARCHAR(1024) USING "name"::VARCHAR(1024);
        ALTER TABLE "task" ALTER COLUMN "description" TYPE VARCHAR(2048) USING "description"::VARCHAR(2048);
        ALTER TABLE "user" DROP COLUMN "otp_recovery";
        ALTER TABLE "project" ALTER COLUMN "description" TYPE VARCHAR(2048) USING "description"::VARCHAR(2048);
        ALTER TABLE "project" ALTER COLUMN "name" TYPE VARCHAR(1024) USING "name"::VARCHAR(1024);
        ALTER TABLE "organization" ALTER COLUMN "name" TYPE VARCHAR(1024) USING "name"::VARCHAR(1024);
        ALTER TABLE "organization" ALTER COLUMN "description" TYPE VARCHAR(2048) USING "description"::VARCHAR(2048);
        ALTER TABLE "organizationmember" ALTER COLUMN "is_admin" TYPE BOOL USING "is_admin"::BOOL;"""
