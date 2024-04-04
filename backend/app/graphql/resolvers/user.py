from typing import Union
from fastapi.requests import HTTPConnection
import strawberry
import bcrypt
from app.models.user import User as UserModel
from app.graphql.types.user import AuthenticatedUser, PublicUser, UserList, User
from app.graphql.types.error import Error
from tortoise.exceptions import DoesNotExist
from dotenv import load_dotenv
import os
from jwt import (
    encode as jwt_encode,
    decode as jwt_decode,
    DecodeError,
    ExpiredSignatureError,
)
from datetime import datetime, timedelta

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
    async def login(
        self, info, name: str, password: str, remember: bool
    ) -> Union[AuthenticatedUser, Error]:
        try:
            user = await UserModel.get(name=name)
            if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                payload = {
                    "exp": datetime.now() + timedelta(days=7 if not remember else 30),
                    "iat": datetime.now(),
                    "sub": user.id,
                }
                token = jwt_encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
                user.token = token
                await user.save()
                return AuthenticatedUser(
                    name=user.name,
                    email=user.email,
                    discord_id=user.discord_id,
                    token=token,
                    isAdmin=user.isAdmin,
                    characters=user.characters,
                )
            else:
                return Error(message="Invalid password")
        except DoesNotExist:
            return Error(message="User does not exist")

    @strawberry.field
    async def register(self, info, name: str, password: str, email: str) -> PublicUser:
        user = await UserModel.create(name=name, password=password, email=email)
        return PublicUser(
            name=user.name,
        )


@strawberry.type
class Query:
    @strawberry.field
    async def me(self, info: strawberry.Private) -> Union[AuthenticatedUser, Error]:
        request: HTTPConnection = info.context["request"]
        token = request.headers.get("Authorization")
        payload = verify_token(token)
        if isinstance(payload, str):
            return Error(message=payload)

        user_id = payload["sub"]
        try:
            user = await UserModel.get(id=user_id).prefetch_related("characters")
            return AuthenticatedUser(
                name=user.name,
                email=user.email,
                discord_id=user.discord_id,
                token=user.token,
                isAdmin=user.isAdmin,
                characters=user.characters,
            )
        except DoesNotExist:
            return Error(message="User does not exist")

    @strawberry.field
    async def users(self, info: strawberry.Private) -> Union[UserList, Error]:
        request: HTTPConnection = info.context["request"]
        token = request.headers.get("Authorization")
        payload = verify_token(token)
        if isinstance(payload, str):
            return Error(message=payload)

        user_id = payload["sub"]
        adminUser = await UserModel.get(id=user_id)

        if not adminUser.isAdmin:
            return Error(message="You are not an admin")

        data = await UserModel.all().prefetch_related("characters")
        print(data[1].characters[0].type)
        users = []
        for user in data:
            users.append(
                User(
                    id=user.id,
                    name=user.name,
                    discord_id=user.discord_id,
                    isAdmin=user.isAdmin,
                    characters=user.characters,
                )
            )
        return UserList(users=users)
