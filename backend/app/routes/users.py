import base64
import bcrypt
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..models import User

class UserIn(BaseModel):
    name: str
    email: str
    password: str
    

class UserOut(BaseModel):
  id: str
  name: str
  recipes_id: Optional[List[int]] = []
  isAdmin: bool

class UserInLogin(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.get("/", response_model=List[UserOut])
async def get_users():
    users = await User.all()
    if not users:
        raise HTTPException(status_code=204, detail="No users found")
    return [UserOut(**user.__dict__) for user in users]

@router.post("/register", response_model=UserOut)
async def create_user(user: UserIn):
    user_obj = await User.create(**user.model_dump())
    return user_obj

@router.post("/login")
async def login_user(user: UserInLogin):
  user_obj = await User.get(email=user.email)
  if not user_obj:
    raise HTTPException(status_code=404, detail="User not found")
  hashed_password = user_obj.password.encode('utf-8')
  passwordInput = user.password.encode('utf-8')
  if bcrypt.checkpw(passwordInput, hashed_password) == False:
    raise HTTPException(status_code=401, detail="Invalid password")
  return True
