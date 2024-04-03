import strawberry
from typing import Optional
from .character import Character


@strawberry.type
class CharacterType:
    id: Optional[str]
    name: str
    experience_rate: Optional[int]
    base_strength: Optional[int]
    base_dexterity: Optional[int]
    base_constitution: Optional[int]
    base_intelligence: Optional[int]
    base_wisdom: Optional[int]
    base_charisma: Optional[int]
    characters: Optional[list[Character]]
