from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from models import Base
if TYPE_CHECKING:    
    from api_v1.submenu.models import Submenu

class Dish(Base):
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[str]

    submenu: Mapped["Submenu"] = relationship(back_populates="dishes", cascade="all, delete")
    submenu_id: Mapped[int] = mapped_column(ForeignKey("submenu.id"), unique=True)
