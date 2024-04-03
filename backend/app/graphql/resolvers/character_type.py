from typing import List, Union
import strawberry
from app.models.character_type import CharacterType as CharacterTypeModel
from app.models.user import User as UserModel
from app.graphql.types.character_type import CharacterType
from app.graphql.types.character import Character
from app.graphql.types.error import Error
from tortoise.exceptions import DoesNotExist
from dotenv import load_dotenv
import os
from jwt import decode as jwt_decode, DecodeError, ExpiredSignatureError

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")


def verify_token(token: str):
    try:
        payload = jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        return "Token has expired"
    except DecodeError:
        return "Invalid token"


@strawberry.type
class Mutation:
    @strawberry.field
    async def create_character_type(
        self, info, token: str, name: str
    ) -> CharacterType:
        payload = verify_token(token)
        if isinstance(payload, str):
            return payload
        character_type = await CharacterTypeModel.create(
            name=name, type=type
        )
        return CharacterType(
            id=character_type.id,
            name=character_type.name,
            experience_rate=character_type.experience_rate,
            base_strength=character_type.base_strength,
            base_dexterity=character_type.base_dexterity,
            base_constitution=character_type.base_constitution,
            base_intelligence=character_type.base_intelligence,
            base_wisdom=character_type.base_wisdom,
            base_charisma=character_type.base_charisma,
            characters=character_type.characters
        )


@strawberry.type
class Query:
    @strawberry.field
    async def characters_type(self, info, token: str) -> list[CharacterType]:
        payload = verify_token(token)
        if isinstance(payload, str):
            return payload
        try:
            charactersTypesData = await CharacterTypeModel.all().prefetch_related("characters")
            charactersTypes = []
            for characterType in charactersTypesData:
                characters = []
                for character in characterType.characters:
                    owner = await UserModel.get(id=character.owner_id)
                    characters.append(
                        Character(
                          id=character.id,
                          name=character.name,
                          level=character.level,
                          type=characterType.name,
                          experience=character.experience,
                          strength=character.strength,
                          dexterity=character.dexterity,
                          constitution=character.constitution,
                          intelligence=character.intelligence,
                          wisdom=character.wisdom,
                          charisma=character.charisma,
                          owner=owner.name,
                        )
                    )
                charactersTypes.append(
                    CharacterType(
                      id=characterType.id,
                      name=characterType.name,
                      experience_rate=characterType.experience_rate,
                      base_strength=characterType.base_strength,
                      base_dexterity=characterType.base_dexterity,
                      base_constitution=characterType.base_constitution,
                      base_intelligence=characterType.base_intelligence,
                      base_wisdom=characterType.base_wisdom,
                      base_charisma=characterType.base_charisma,
                      characters=characters
                    )
                )
            return charactersTypes
        except DoesNotExist:
            return Error(message="Character type does not exist")
