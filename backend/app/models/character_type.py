import uuid
from tortoise.models import Model
from tortoise import fields
from tortoise.signals import pre_save

class CharacterType(Model):
  id = fields.CharField(pk=True, max_length=255)
  name = fields.CharField(max_length=255)
  experience_rate = fields.IntField(default=1)
  base_strength = fields.IntField(default=1)
  base_dexterity = fields.IntField(default=1)
  base_constitution = fields.IntField(default=1)
  base_intelligence = fields.IntField(default=1)
  base_wisdom = fields.IntField(default=1)
  base_charisma = fields.IntField(default=1)

@pre_save(CharacterType)
async def generate_uuid(sender, instance, using_db, update_fields):
    if not instance.id:
        instance.id = str(uuid.uuid4())