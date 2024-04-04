from decimal import Decimal
import strawberry
from typing import Optional


@strawberry.type
class Character:
    id: Optional[str]
    name: Optional[str]
    level: Optional[int]
    experience: Optional[Decimal]
    strength: Optional[int]
    dexterity: Optional[int]
    constitution: Optional[int]
    intelligence: Optional[int]
    wisdom: Optional[int]
    charisma: Optional[int]
    owner: Optional[str]


@strawberry.type
class CharacterType:
    id: Optional[str]
    name: str
    experience_rate: Optional[Decimal]
    base_strength: Optional[int]
    base_dexterity: Optional[int]
    base_constitution: Optional[int]
    base_intelligence: Optional[int]
    base_wisdom: Optional[int]
    base_charisma: Optional[int]


@strawberry.type
class CharacterOutput(Character):
    type: Optional[CharacterType]


@strawberry.type
class CharacterTypeOutput(CharacterType):
    characters: Optional[list[Character]]


@strawberry.type
class CharacterOutputList:
    characters: list[CharacterOutput]


@strawberry.type
class CharacterTypeOutputList:
    character_types: list[CharacterTypeOutput]
