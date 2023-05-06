from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "file" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "size" BIGINT NOT NULL,
    "path" VARCHAR(1024) NOT NULL,
    "is_dir" BOOL NOT NULL,
    "project_id" UUID NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "file"."id" IS 'File ID';;
        CREATE TABLE IF NOT EXISTS "idea" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(1024) NOT NULL,
    "description" TEXT NOT NULL,
    "project_id" UUID NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "idea"."id" IS 'Idea ID';;
        ALTER TABLE "project" ADD "logo" UUID;
        ALTER TABLE "task" ALTER COLUMN "description" TYPE TEXT USING "description"::TEXT;
        ALTER TABLE "task" ALTER COLUMN "description" TYPE TEXT USING "description"::TEXT;
        ALTER TABLE "task" ALTER COLUMN "description" TYPE TEXT USING "description"::TEXT;
        ALTER TABLE "user" ADD "logo" UUID;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "task" ALTER COLUMN "description" TYPE VARCHAR(2048) USING "description"::VARCHAR(2048);
        ALTER TABLE "task" ALTER COLUMN "description" TYPE VARCHAR(2048) USING "description"::VARCHAR(2048);
        ALTER TABLE "task" ALTER COLUMN "description" TYPE VARCHAR(2048) USING "description"::VARCHAR(2048);
        ALTER TABLE "user" DROP COLUMN "logo";
        ALTER TABLE "project" DROP COLUMN "logo";
        DROP TABLE IF EXISTS "file";
        DROP TABLE IF EXISTS "idea";"""
