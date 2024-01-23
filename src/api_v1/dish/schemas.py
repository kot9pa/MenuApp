from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str
    price: str

class Dish(DishBase):
    id: int

class DishCreate(DishBase):
    pass

class DishUpdate(DishCreate):
    pass

class DishUpdatePartial(DishCreate):
    title: str | None = None
    description: str | None = None
    price: str | None = None
