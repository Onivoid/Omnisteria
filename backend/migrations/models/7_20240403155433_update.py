from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "charactertype" ALTER COLUMN "base_dexterity" DROP DEFAULT;
        ALTER TABLE "charactertype" ALTER COLUMN "base_intelligence" DROP DEFAULT;
        ALTER TABLE "charactertype" ALTER COLUMN "base_wisdom" DROP DEFAULT;
        ALTER TABLE "charactertype" ALTER COLUMN "base_charisma" DROP DEFAULT;
        ALTER TABLE "charactertype" ALTER COLUMN "base_constitution" DROP DEFAULT;
        ALTER TABLE "charactertype" ALTER COLUMN "experience_rate" DROP DEFAULT;
        ALTER TABLE "charactertype" ALTER COLUMN "base_strength" DROP DEFAULT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "charactertype" ALTER COLUMN "base_dexterity" SET DEFAULT 1;
        ALTER TABLE "charactertype" ALTER COLUMN "base_intelligence" SET DEFAULT 1;
        ALTER TABLE "charactertype" ALTER COLUMN "base_wisdom" SET DEFAULT 1;
        ALTER TABLE "charactertype" ALTER COLUMN "base_charisma" SET DEFAULT 1;
        ALTER TABLE "charactertype" ALTER COLUMN "base_constitution" SET DEFAULT 1;
        ALTER TABLE "charactertype" ALTER COLUMN "experience_rate" SET DEFAULT 1;
        ALTER TABLE "charactertype" ALTER COLUMN "base_strength" SET DEFAULT 1;"""
