import strawberry
from typing import Optional
from .character import Character


@strawberry.type
class PublicUser:
    name: str


@strawberry.type
class AuthenticatedUser:
    name: str
    email: Optional[str]
    discord_id: Optional[int]
    token: Optional[str]
    characters: Optional[list[Character]]
