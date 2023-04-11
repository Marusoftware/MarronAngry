from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "uid_user_name_76f409";
        ALTER TABLE "user" ADD "otp_status" VARCHAR(9) NOT NULL  DEFAULT 'inactive';
        ALTER TABLE "user" DROP COLUMN "fullname";
        ALTER TABLE "user" ALTER COLUMN "otp_recovery" TYPE VARCHAR(84) USING "otp_recovery"::VARCHAR(84);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "fullname" VARCHAR(1024) NOT NULL  DEFAULT '';
        ALTER TABLE "user" DROP COLUMN "otp_status";
        ALTER TABLE "user" ALTER COLUMN "otp_recovery" TYPE VARCHAR(6) USING "otp_recovery"::VARCHAR(6);
        CREATE UNIQUE INDEX "uid_user_name_76f409" ON "user" ("name");"""
