import os
from dotenv import load_dotenv
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from .routes import router

load_dotenv('../config/.env')

app = FastAPI()

app.include_router(router, prefix="/api")

register_tortoise(
    app,
    db_url=os.getenv('DATABASE_URL'),
    modules={'models': ['app.models.user']},
    generate_schemas=True,
    add_exception_handlers=True,
)