from pydantic import BaseModel

from api_v1.menu.schemas import Menu


class SubmenuBase(BaseModel):
    title: str
    description: str    

class Submenu(SubmenuBase):
    id: int

class SubmenuCreate(SubmenuBase):
    pass

class SubmenuUpdate(SubmenuCreate):
    pass

class SubmenuUpdatePartial(SubmenuCreate):
    title: str | None = None
    description: str | None = None