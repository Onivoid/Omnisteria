from typing import Union, Optional
from decimal import Decimal
from fastapi.requests import HTTPConnection
import strawberry
from app.models.character import Character as CharacterModel
from app.models.character_type import CharacterType as CharacterTypeModel
from app.graphql.types.character import (
    CharacterOutput,
    CharacterOutputList,
    CharacterTypeOutput,
    CharacterTypeOutputList,
)
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


async def create_character_output(character):
    owner = (
        await CharacterModel.get(id=character.id).prefetch_related("owner")
    ).owner.name
    return CharacterOutput(
        id=character.id,
        name=character.name,
        level=character.level,
        experience=character.experience,
        type=character.type,
        strength=character.strength,
        dexterity=character.dexterity,
        constitution=character.constitution,
        intelligence=character.intelligence,
        wisdom=character.wisdom,
        charisma=character.charisma,
        owner=owner,
    )


@strawberry.type
class Mutation:
    @strawberry.field
    async def create_character(
        self, info: strawberry.Private, name: str, type: str
    ) -> Union[CharacterOutput, Error]:
        request: HTTPConnection = info.context["request"]
        token = request.headers.get("Authorization")
        payload = verify_token(token)
        if isinstance(payload, str):
            return Error(message=payload)

        user_id = payload["sub"]
        character_type = await CharacterTypeModel.get(name=type)
        if not character_type:
            return Error(message="Character type does not exist")
        try:
            character = await CharacterModel.create(
                name=name,
                type_id=character_type.id,
                owner_id=user_id,
                strength=character_type.base_strength,
                dexterity=character_type.base_dexterity,
                constitution=character_type.base_constitution,
                intelligence=character_type.base_intelligence,
                wisdom=character_type.base_wisdom,
                charisma=character_type.base_charisma,
            )
            return CharacterOutput(
                id=character.id,
                name=character.name,
                level=character.level,
                experience=character.experience,
                type=character.type,
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

    @strawberry.field
    async def create_character_type(
        self,
        info: strawberry.Private,
        name: str,
        experience_rate: Optional[Decimal] = None,
        base_strength: Optional[int] = None,
        base_dexterity: Optional[int] = None,
        base_constitution: Optional[int] = None,
        base_intelligence: Optional[int] = None,
        base_wisdom: Optional[int] = None,
        base_charisma: Optional[int] = None,
    ) -> Union[CharacterTypeOutput, Error]:
        request: HTTPConnection = info.context["request"]
        token = request.headers.get("Authorization")
        payload = verify_token(token)
        if isinstance(payload, str):
            return Error(message=payload)
        character_type = await CharacterTypeModel.create(
            name=name,
            type=type,
            experience_rate=experience_rate if experience_rate else "1.0",
            base_strength=base_strength if base_strength else 1,
            base_dexterity=base_dexterity if base_dexterity else 1,
            base_constitution=base_constitution if base_constitution else 1,
            base_intelligence=base_intelligence if base_intelligence else 1,
            base_wisdom=base_wisdom if base_wisdom else 1,
            base_charisma=base_charisma if base_charisma else 1,
        )
        return CharacterTypeOutput(
            id=character_type.id,
            name=character_type.name,
            experience_rate=character_type.experience_rate,
            base_strength=character_type.base_strength,
            base_dexterity=character_type.base_dexterity,
            base_constitution=character_type.base_constitution,
            base_intelligence=character_type.base_intelligence,
            base_wisdom=character_type.base_wisdom,
            base_charisma=character_type.base_charisma,
            characters=character_type.characters,
        )


@strawberry.type
class Query:
    @strawberry.field
    async def characters(
        self, info: strawberry.Private
    ) -> Union[CharacterOutputList, Error]:
        request: HTTPConnection = info.context["request"]
        token = request.headers.get("Authorization")
        payload = verify_token(token)
        if isinstance(payload, str):
            return Error(message=payload)
        try:
            charactersData = await CharacterModel.all().prefetch_related("owner")
            characters = [
                await create_character_output(character) for character in charactersData
            ]
            return characters
        except DoesNotExist:
            return Error(message="Character does not exist")

    @strawberry.field
    async def characters_type(
        self, info: strawberry.Private
    ) -> Union[CharacterTypeOutputList, Error]:
        request: HTTPConnection = info.context["request"]
        token = request.headers.get("Authorization")
        payload = verify_token(token)
        if isinstance(payload, str):
            return Error(message=payload)
        try:
            charactersTypesData = await CharacterTypeModel.all().prefetch_related(
                "characters"
            )
            charactersTypes = []
            for characterType in charactersTypesData:
                characters = [
                    await create_character_output(character)
                    for character in characterType.characters
                ]
                charactersTypes.append(
                    CharacterTypeOutput(
                        id=characterType.id,
                        name=characterType.name,
                        experience_rate=characterType.experience_rate,
                        base_strength=characterType.base_strength,
                        base_dexterity=characterType.base_dexterity,
                        base_constitution=characterType.base_constitution,
                        base_intelligence=characterType.base_intelligence,
                        base_wisdom=characterType.base_wisdom,
                        base_charisma=characterType.base_charisma,
                        characters=characters,
                    )
                )
            return charactersTypes
        except DoesNotExist:
            return Error(message="Character type does not exist")
