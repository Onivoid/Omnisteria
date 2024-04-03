from .config import TORTOISE_ORM
from dotenv import load_dotenv
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from strawberry.asgi import GraphQL
import strawberry
from .graphql.resolvers.user import Query as UserQuery, Mutation as UserMutation
from .graphql.resolvers.character import (
    Query as CharacterQuery,
    Mutation as CharacterMutation,
)
from .graphql.resolvers.character_type import (
    Query as CharacterTypeQuery,
    Mutation as CharacterTypeMutation,
)

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
]


@strawberry.type
class Query(UserQuery, CharacterQuery, CharacterTypeQuery):
    pass


@strawberry.type
class Mutation(UserMutation, CharacterMutation, CharacterTypeMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)

app.add_route("/graphql", GraphQL(schema=schema))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
