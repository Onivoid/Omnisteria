from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..models import Character

router = APIRouter()

class CharacterIn(BaseModel):
    name: str
    owner_id: str
    type: str

@router.get("/")
async def get_characters():
    characters = await Character.all()
    if not characters:
        raise HTTPException(status_code=204, detail="No characters found")
    return characters

@router.post("/create")
async def create_character(character: CharacterIn):
    character_obj = await Character.create(**character.model_dump())
    return character_obj
