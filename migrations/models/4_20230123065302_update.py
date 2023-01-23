from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE "project_organizationmember" (
    "organizationmember_id" UUID NOT NULL REFERENCES "organizationmember" ("id") ON DELETE CASCADE,
    "project_id" UUID NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE
);
        CREATE TABLE "task_organizationmember" (
    "task_id" UUID NOT NULL REFERENCES "task" ("id") ON DELETE CASCADE,
    "organizationmember_id" UUID NOT NULL REFERENCES "organizationmember" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "project_organizationmember";
        DROP TABLE IF EXISTS "task_organizationmember";"""
