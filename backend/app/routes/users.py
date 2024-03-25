import bcrypt
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..models import User, Character
from tortoise.contrib.pydantic import pydantic_model_creator

CharacterType = pydantic_model_creator(Character, name="Character")


class UserIn(BaseModel):
    name: str
    email: str
    password: str
    

class UserOut(BaseModel):
  id: str
  name: str
  isAdmin: bool
  characters: List[CharacterType] = [] # type: ignore

class UserInLogin(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.get("/", response_model=List[UserOut])
async def get_users():
    users = await User.all().prefetch_related("characters")
    user_outs = []
    for user in users:
        user_out = UserOut(**user.__dict__)
        user_out.characters = [await CharacterType.from_tortoise_orm(character) for character in user.characters]
        user_outs.append(user_out)
    if not user_outs:
        raise HTTPException(status_code=204, detail="No users found")
    return user_outs

@router.post("/register", response_model=UserOut)
async def create_user(user: UserIn):
    user_obj = await User.create(**user.model_dump())
    return UserOut(**user_obj.__dict__)

@router.post("/login", response_model=UserOut)
async def login_user(user: UserInLogin):
  user_finded = await User.get(email=user.email)
  if not user_finded:
    raise HTTPException(status_code=404, detail="User not found")
  hashed_password = user_finded.password.encode('utf-8')
  passwordInput = user.password.encode('utf-8')
  if bcrypt.checkpw(passwordInput, hashed_password) == False:
    raise HTTPException(status_code=401, detail="Invalid password")
  await user_finded.fetch_related("characters")
  result = UserOut(**user_finded.__dict__)
  result.characters = [await CharacterType.from_tortoise_orm(character) for character in user_finded.characters]
  
  return result
