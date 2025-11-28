from pydantic import BaseModel

class UserDietInfo(BaseModel):
    user_id: int
    age: int
    sex: int
    height: float
    weight: float
    total_kcal: float
    total_carbs: float
    total_fat: float
    total_protein: float
    total_sodium: float
    total_sugar: float
