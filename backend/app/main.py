import os
from dotenv import load_dotenv
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from .routes import router
from fastapi.middleware.cors import CORSMiddleware

load_dotenv('../../.env')

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.include_router(router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    db_url=os.getenv('DATABASE_URL'),
    modules={'models': ['app.models.user', 'app.models.character']},
    generate_schemas=True,
    add_exception_handlers=True,
)