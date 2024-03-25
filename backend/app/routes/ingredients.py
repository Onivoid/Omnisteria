from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..models import Ingredient

class IngredientIn(BaseModel):
    name: str
    image_url: str = "https://placehold.co/1080x1080"
    price: float = 0
    portion_size: float
    kcal: float
    proteins: float
    carbohydrate: float
    fats: float

class IngredientOut(IngredientIn):
    id: int

    class Config:
        from_attributes = True

router = APIRouter()

@router.get("/", response_model=List[IngredientOut])
async def get_ingredients():
    ingredients = await Ingredient.all()
    if not ingredients:
        raise HTTPException(status_code=204, detail="No ingredients found")
    return ingredients

@router.post("/", response_model=IngredientOut)
async def create_ingredient(ingredient: IngredientIn):
    ingredient_obj = await Ingredient.create(**ingredient.model_dump())
    return ingredient_obj