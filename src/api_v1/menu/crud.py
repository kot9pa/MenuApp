from statistics import mean
from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Menu
from .schemas import MenuView, MenuCreate, MenuUpdate, MenuUpdatePartial


async def get_menus(session: AsyncSession) -> list[MenuView]:
    stmt = select(Menu).order_by(Menu.id)    
    result: Result = await session.execute(stmt)
    menus = result.scalars().all()
    for m in menus:
        print(m.submenus_count)
        print(m.dishes_count)
    return list(menus)

async def get_menu(session: AsyncSession, menu_id: int) -> Menu | None:
    return await session.get(Menu, menu_id)

async def create_menu(session: AsyncSession, menu_in: MenuCreate) -> Menu:
    menu = Menu(**menu_in.model_dump())
    session.add(menu)
    await session.commit()
    # await session.refresh(menu)
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