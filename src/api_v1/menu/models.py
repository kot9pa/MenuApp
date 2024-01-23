from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from models import Base
if TYPE_CHECKING:    
    from api_v1.submenu.models import Submenu


class Menu(Base):
    title: Mapped[str]
    description: Mapped[str]

    submenus: Mapped[List["Submenu"]] = relationship(back_populates="menu", cascade="all, delete")

    @hybrid_property
    def submenus_count(self):
        return 0
    
    @hybrid_property
    def dishes_count(self):
        return 0
    