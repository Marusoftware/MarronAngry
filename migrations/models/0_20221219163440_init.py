from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "oauth" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "provider" VARCHAR(100) NOT NULL,
    "token1" VARCHAR(200) NOT NULL,
    "token2" VARCHAR(200) NOT NULL,
    "is_oauth2" BOOL NOT NULL  DEFAULT False,
    "expires_at" TIMESTAMPTZ
);
COMMENT ON COLUMN "oauth"."id" IS 'OAuth ID';
COMMENT ON COLUMN "oauth"."provider" IS 'OAuth Provider';
CREATE TABLE IF NOT EXISTS "user" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(1024) NOT NULL UNIQUE,
    "fullname" VARCHAR(1024) NOT NULL  DEFAULT '',
    "is_dev" BOOL NOT NULL  DEFAULT False,
    "email" VARCHAR(1024) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_user_name_76f409" ON "user" ("name");
COMMENT ON COLUMN "user"."id" IS 'User ID';
COMMENT ON COLUMN "user"."name" IS 'User short name';
COMMENT ON COLUMN "user"."fullname" IS 'User long name';
COMMENT ON COLUMN "user"."is_dev" IS 'Is this user developer?';
COMMENT ON COLUMN "user"."email" IS 'User email';
CREATE TABLE IF NOT EXISTS "auth" (
    "password" VARCHAR(1024),
    "user_id" UUID NOT NULL  PRIMARY KEY REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "auth"."password" IS 'User password';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
