import uuid
import bcrypt
from tortoise.models import Model
from tortoise import fields
from tortoise.signals import pre_save
from .character import Character


class User(Model):
    id = fields.CharField(pk=True, max_length=255)
    name = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    discord_id = fields.IntField(null=True)
    password = fields.CharField(max_length=255, null=True)
    isAdmin = fields.BooleanField(default=False)
    token = fields.CharField(max_length=255, null=True)


@pre_save(User)
async def generate_uuid(sender, instance, using_db, update_fields):
    if not instance.id:
        instance.id = str(uuid.uuid4())


@pre_save(User)
async def hash_password(sender, instance, using_db, update_fields):
    if not instance.password.startswith("$2b$"):
        instance.password = bcrypt.hashpw(
            instance.password.encode("utf8"), bcrypt.gensalt()
        ).decode("utf8")
