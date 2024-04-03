from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "character" ALTER COLUMN "experience" TYPE DECIMAL(10,2) USING "experience"::DECIMAL(10,2);
        ALTER TABLE "character" ALTER COLUMN "experience" TYPE DECIMAL(10,2) USING "experience"::DECIMAL(10,2);
        ALTER TABLE "charactertype" ALTER COLUMN "experience_rate" TYPE DECIMAL(5,2) USING "experience_rate"::DECIMAL(5,2);
        ALTER TABLE "charactertype" ALTER COLUMN "experience_rate" TYPE DECIMAL(5,2) USING "experience_rate"::DECIMAL(5,2);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "character" ALTER COLUMN "experience" TYPE INT USING "experience"::INT;
        ALTER TABLE "charactertype" ALTER COLUMN "experience_rate" TYPE INT USING "experience_rate"::INT;"""
