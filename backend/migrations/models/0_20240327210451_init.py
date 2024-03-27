from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" VARCHAR(255) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255)  UNIQUE,
    "discord_id" INT,
    "password" VARCHAR(255),
    "isAdmin" BOOL NOT NULL  DEFAULT False,
    "token" VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS "character" (
    "id" VARCHAR(255) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "level" INT NOT NULL  DEFAULT 1,
    "experience" INT NOT NULL  DEFAULT 0,
    "type" VARCHAR(255) NOT NULL,
    "strength" INT NOT NULL  DEFAULT 1,
    "dexterity" INT NOT NULL  DEFAULT 1,
    "constitution" INT NOT NULL  DEFAULT 1,
    "intelligence" INT NOT NULL  DEFAULT 1,
    "wisdom" INT NOT NULL  DEFAULT 1,
    "charisma" INT NOT NULL  DEFAULT 1,
    "owner_id" VARCHAR(255) NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
