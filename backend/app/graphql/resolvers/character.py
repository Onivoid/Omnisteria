from typing import Union
import strawberry
from app.models.character import Character as CharacterModel
from app.models.user import User as UserModel
from app.models.character_type import CharacterType as CharacterTypeModel
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
    async def create_character(
        self, info, token: str, name: str, type: str
    ) -> Union[Character, Error]:
        payload = verify_token(token)
        if isinstance(payload, str):
            return Error(message="Token Error")

        user_id = payload["sub"]
        character_type = await CharacterTypeModel.get(name=type)
        if not character_type:
            return Error(message="Character type does not exist")
        try:
            character = await CharacterModel.create(
                name=name, type_id=character_type.id, owner_id=user_id
            )
            return Character(
                id=character.id,
                name=character.name,
                level=character.level,
                experience=character.experience,
                type=character_type.name,
                strength=character.strength,
                dexterity=character.dexterity,
                constitution=character.constitution,
                intelligence=character.intelligence,
                wisdom=character.wisdom,
                charisma=character.charisma,
                owner=character.owner_id,
            )
        except Exception as e:
            return Error(message=str(e))


@strawberry.type
class Query:
    @strawberry.field
    async def characters(self, info, token: str) -> list[Character]:
        payload = verify_token(token)
        if isinstance(payload, str):
            return payload
        try:
            charactersData = await CharacterModel.all()
            characters = []
            for character in charactersData:
                owner = await UserModel.get(id=character.owner_id)
                character_type = await CharacterTypeModel.get(id=character.type_id)
                characters.append(
                    Character(
                        id=character.id,
                        name=character.name,
                        level=character.level,
                        experience=character.experience,
                        type=character_type.name,
                        strength=character.strength,
                        dexterity=character.dexterity,
                        constitution=character.constitution,
                        intelligence=character.intelligence,
                        wisdom=character.wisdom,
                        charisma=character.charisma,
                        owner=owner.name,
                    )
                )
            return characters
        except DoesNotExist:
            return "User does not exist"
