from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from models import Base
if TYPE_CHECKING:    
    from api_v1.menu.models import Menu
    from api_v1.dish.models import Dish


class Submenu(Base):
    title: Mapped[str]
    description: Mapped[str]

    menu: Mapped["Menu"] = relationship(back_populates="submenus", cascade="all, delete")
    menu_id: Mapped[int] = mapped_column(ForeignKey("menu.id"), unique=True)
    dishes: Mapped[List["Dish"]] = relationship(back_populates="submenu", cascade="all, delete")
