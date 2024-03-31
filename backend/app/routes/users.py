import bcrypt
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from ..models import User, Character
from tortoise.contrib.pydantic import pydantic_model_creator
from jwt import (
    encode as jwt_encode,
    decode as jwt_decode,
    PyJWTError as JWTError,
    ExpiredSignatureError as ExpiredError,
)
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")

CharacterType = pydantic_model_creator(Character, name="Character")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserIn(BaseModel):
    name: str
    email: str
    password: str


class UserOut(BaseModel):
    id: str
    name: str
    isAdmin: bool
    characters: List[CharacterType] = []  # type: ignore


class UserInLogin(BaseModel):
    email: str
    password: str
    stayLog: bool = False


class UserOutLogin(BaseModel):
    token: str


router = APIRouter()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> Optional[UserOutLogin]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = await User.get(id=payload["sub"])
        if user is None:
            raise credentials_exception
        return user
    except ExpiredError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise credentials_exception


@router.get("/me")
async def test_route(user: UserOutLogin = Depends(get_current_user)):
    if user.isAdmin:
        return {"message": "You are an admin"}
    else:
        return {"message": "You are not an admin"}


@router.get("/", response_model=List[UserOut])
async def get_users():
    users = await User.all().prefetch_related("characters")
    user_outs = []
    for user in users:
        user_out = UserOut(**user.__dict__)
        user_out.characters = [
            await CharacterType.from_tortoise_orm(character)
            for character in user.characters
        ]
        user_outs.append(user_out)
    if not user_outs:
        raise HTTPException(status_code=204, detail="No users found")
    return user_outs


@router.post("/register", response_model=UserOut)
async def create_user(user: UserIn):
    user_obj = await User.create(**user.model_dump())
    return UserOut(**user_obj.__dict__)


@router.post("/login", response_model=UserOutLogin)
async def login_user(user: UserInLogin):
    user_finded = await User.get(email=user.email)
    if not user_finded:
        raise HTTPException(status_code=404, detail="User not found")
    hashed_password = user_finded.password.encode("utf-8")
    passwordInput = user.password.encode("utf-8")
    if bcrypt.checkpw(passwordInput, hashed_password) == False:
        raise HTTPException(status_code=401, detail="Invalid password")
    #await user_finded.fetch_related("characters")

    payload = {
        "exp": datetime.now() + timedelta(seconds=10 if not user.stayLog else 30),
        "iat": datetime.now(),
        "sub": user_finded.id,
    }

    token = jwt_encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)

    user_finded.token = token

    await user_finded.save()

    result = UserOutLogin(**user_finded.__dict__)
    #result.characters = [
    #    await CharacterType.from_tortoise_orm(character)
    #    for character in user_finded.characters
    #]

    result.token = token

    return result

@router.post("/logout")
async def logout_user(user: UserOutLogin = Depends(get_current_user)):
    user.token = None
    await user.save()
    return {"message": "Logged out"}