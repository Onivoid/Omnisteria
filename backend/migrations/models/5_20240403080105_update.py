from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "character" RENAME COLUMN "type" TO "type_id";
        CREATE TABLE IF NOT EXISTS "charactertype" (
    "id" VARCHAR(255) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "experience_rate" INT NOT NULL  DEFAULT 1,
    "base_strength" INT NOT NULL  DEFAULT 1,
    "base_dexterity" INT NOT NULL  DEFAULT 1,
    "base_constitution" INT NOT NULL  DEFAULT 1,
    "base_intelligence" INT NOT NULL  DEFAULT 1,
    "base_wisdom" INT NOT NULL  DEFAULT 1,
    "base_charisma" INT NOT NULL  DEFAULT 1
);
        ALTER TABLE "character" ADD CONSTRAINT "fk_characte_characte_f2f5b6a7" FOREIGN KEY ("type_id") REFERENCES "charactertype" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "character" DROP CONSTRAINT "fk_characte_characte_f2f5b6a7";
        ALTER TABLE "character" RENAME COLUMN "type_id" TO "type";
        DROP TABLE IF EXISTS "charactertype";"""
