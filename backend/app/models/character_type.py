import uuid
from tortoise.models import Model
from tortoise import fields
from tortoise.signals import pre_save


class CharacterType(Model):
    id = fields.CharField(pk=True, max_length=255)
    name = fields.CharField(max_length=255)
    experience_rate = fields.DecimalField(max_digits=5, decimal_places=2)
    base_strength = fields.IntField()
    base_dexterity = fields.IntField()
    base_constitution = fields.IntField()
    base_intelligence = fields.IntField()
    base_wisdom = fields.IntField()
    base_charisma = fields.IntField()


@pre_save(CharacterType)
async def generate_uuid(sender, instance, using_db, update_fields):
    if not instance.id:
        instance.id = str(uuid.uuid4())
