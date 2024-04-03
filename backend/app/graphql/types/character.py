from decimal import Decimal
import strawberry
from typing import Optional


@strawberry.type
class Character:
    id: Optional[str]
    name: Optional[str]
    level: Optional[int]
    experience: Optional[Decimal]
    type: Optional[str]
    strength: Optional[int]
    dexterity: Optional[int]
    constitution: Optional[int]
    intelligence: Optional[int]
    wisdom: Optional[int]
    charisma: Optional[int]
    owner: Optional[str]
