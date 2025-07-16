from pydantic import BaseModel
from typing import Optional,List,Dict
from enum import Enum
from datetime import datetime,date
from uuid import UUID
class TokenData(BaseModel):
    uid: str
    email: Optional[str] = None

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    uid: str
    disabled: bool = False

class ProtectedResponse(BaseModel):
    message: str
    user_info: dict

class NutrientInfo(BaseModel):
    protein_g: float
    carbohydrates_g: float
    fats_g: float

class FoodItem(BaseModel):
    name: str
    calories_per_gram: float
    nutrients: NutrientInfo


class CalorieAnalysisResponse(BaseModel):
    items: List[FoodItem]
    healthy_alternatives: str  # Optional


class Nutrients(BaseModel):
    protein_g: float
    carbohydrates_g: float
    fats_g: float

class FoodItem(BaseModel):
    name: str
    calories: float
    nutrients: Nutrients
    serving_size: Optional[str] = None




class Gender(str, Enum):
    male = "male"
    female = "female"

class ActivityLevel(str, Enum):
    sedentary = "sedentary"
    light = "light"
    moderate = "moderate"
    active = "active"
    extra = "extra"

class Goal(str, Enum):
    lose = "lose"
    maintain = "maintain"
    gain = "gain"
    custom="custom"

class UserProfileCreate(BaseModel):
    name:str
    age: int
    gender: Gender
    weight_kg: float
    height_cm: float
    activity_level: ActivityLevel
    goal: Goal
    customCalorie: Optional[int] = None 
    
class UserOut(BaseModel):
    id: str
    email: str
    name: Optional[str]
    is_active: bool
    age: int
    gender: str
    weight_kg: float
    height_cm: float
    activity_level: str
    goal: str
    target_calories: Optional[int]
    created_at: datetime  # <-- Fix: must be datetime, not str

    class Config:
        from_attributes = True
class UserProfileResponse(UserProfileCreate):
    id: str
    target_calories: Optional[int]
    created_at: str




class NutrientInfo(BaseModel):
    protein_g: float
    carbohydrates_g: float
    fats_g: float

class FoodItem(BaseModel):
    name: str
    calories_per_gram: float
    nutrients: NutrientInfo

class LoggedFoodItem(FoodItem):
    weight_grams: float
    # calculated_calories: float

class FoodLogCreate(BaseModel):
    food_name: str
    weight_grams: float
    calories_per_gram: float
    nutrients: NutrientInfo
    meal_type: Optional[str] = None
    notes: Optional[str] = None

class FoodLogResponse(BaseModel):
    id: UUID
    user_id: str
    food_name: str
    weight_grams: float
    calories_consumed: float
    protein_g: float
    carbs_g: float
    fats_g: float
    meal_type: Optional[str]
    logged_at: datetime
    image_url: Optional[str]

class Config:
    from_attributes = True


class FoodLogBatchCreate(BaseModel):
    items: List[LoggedFoodItem]  # Reusing your existing LoggedFoodItem
    meal_type: str = None
    notes: str = None
    image_url: str = None  # Optional reference to scanned image
    
class DailyNutritionSummary(BaseModel):
    date: date
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fats: float

class DailyNutritionSummary(BaseModel):
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fats: float

class MonthlyNutritionResponse(BaseModel):
    year: int
    month: int
    daily_summaries: Dict[date, DailyNutritionSummary]

    # In your schemas file (src/models/schemas.py)



class FoodItemDetail(BaseModel):
    id: str
    food_name: str
    weight_grams: float
    calories_consumed: float
    protein_g: float
    carbs_g: float
    fats_g: float
    meal_type: str | None
    logged_at: datetime
    notes: str | None
    image_url: str | None


class DailyDetailsResponse(BaseModel):
    date: date
    summary: DailyNutritionSummary
    items: List[FoodItemDetail]