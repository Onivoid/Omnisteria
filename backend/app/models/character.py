import uuid
from tortoise.models import Model
from tortoise import fields
from tortoise.signals import pre_save


class Character(Model):
    id = fields.CharField(pk=True, max_length=255)
    name = fields.CharField(max_length=255)
    level = fields.IntField(default=1)
    experience = fields.IntField(default=0)
    type = fields.ForeignKeyField("models.CharacterType", related_name="characters")
    strength = fields.IntField(default=1)
    dexterity = fields.IntField(default=1)
    constitution = fields.IntField(default=1)
    intelligence = fields.IntField(default=1)
    wisdom = fields.IntField(default=1)
    charisma = fields.IntField(default=1)
    owner = fields.ForeignKeyField(
        "models.User", related_name="characters", on_delete=fields.CASCADE
    )


@pre_save(Character)
async def generate_uuid(sender, instance, using_db, update_fields):
    if not instance.id:
        instance.id = str(uuid.uuid4())
