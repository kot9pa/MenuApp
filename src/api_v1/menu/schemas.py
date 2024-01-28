from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str

class Menu(MenuBase):
    id: int

class MenuView(Menu):
    submenus_count: int | None = None
    dishes_count: int | None = None

class MenuCreate(MenuBase):
    pass

class MenuUpdate(MenuCreate):
    pass

class MenuUpdatePartial(MenuCreate):
    title: str | None = None
    description: str | None = None
