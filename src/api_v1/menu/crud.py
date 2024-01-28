from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Menu
from api_v1.submenu.models import Submenu
from .schemas import MenuCreate, MenuUpdate, MenuUpdatePartial


async def get_menus(session: AsyncSession) -> list[Menu]:
    stmt = select(Menu)
    result = await session.scalars(stmt)
    return list(result)

async def get_menu(session: AsyncSession, menu_id: int) -> Menu | None:
    stmt = select(Menu).where(Menu.id == menu_id)
    return await session.scalar(stmt)

async def get_menu_with_counts(session: AsyncSession, menu_in: Menu = None) -> list[Menu]:
    menus = list()
    if menu_in is None:
        result = await session.scalars(select(Menu).options(joinedload(Menu.submenus)
                                .selectinload(Submenu.dishes)))
    else:
        result = await session.scalars(select(Menu).options(joinedload(Menu.submenus)
                                .selectinload(Submenu.dishes)).where(Menu.id == menu_in.id))
    for r in result.unique():
        menu = Menu(
            id = r.id,
            title = r.title,
            description = r.description
        )
        menu.submenus_count = len(r.submenus)
        menu.dishes_count = sum(len(s.dishes) for s in r.submenus)
        menus.append(menu)
    return list(menus)

async def create_menu(session: AsyncSession, menu_in: MenuCreate) -> Menu:
    menu = Menu(**menu_in.model_dump(exclude_none=True))
    session.add(menu)
    await session.commit()
    return menu

async def update_menu(session: AsyncSession, 
                      menu: Menu, menu_update: MenuUpdate | MenuUpdatePartial,
                      partial: bool = False) -> Menu:
    for key, value in menu_update.model_dump(exclude_unset=partial).items():
        setattr(menu, key, value)
    await session.commit()
    return menu

async def delete_menu(session: AsyncSession, menu: Menu) -> None:
    await session.delete(menu)
    await session.commit()