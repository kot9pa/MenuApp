from pydantic import BaseModel


class SubmenuBase(BaseModel):
    title: str
    description: str    

class Submenu(SubmenuBase):
    id: int

class SubmenuView(Submenu):
    dishes_count: int | None = None

class SubmenuCreate(SubmenuBase):
    pass

class SubmenuUpdate(SubmenuCreate):
    pass

class SubmenuUpdatePartial(SubmenuCreate):
    title: str | None = None
    description: str | None = None