from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.menu.models import Menu
from .models import Submenu
from .schemas import SubmenuCreate, SubmenuUpdate, SubmenuUpdatePartial


async def get_submenus(session: AsyncSession, menu_id: int) -> list[Submenu]:
    stmt = select(Submenu).where(Submenu.menu_id == menu_id)
    result = await session.scalars(stmt)
    return list(result)

async def get_submenu(session: AsyncSession, menu_id: int, submenu_id: int) -> Submenu | None:
    stmt = select(Submenu).where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
    return await session.scalar(stmt)

async def get_submenu_with_counts(session: AsyncSession, menu_in: Menu, submenu_in: Submenu = None) -> list[Submenu]:    
    submenus = list()
    if submenu_in is None:
        result = await session.scalars(select(Submenu).options(joinedload(Submenu.dishes))
                                       .where(Submenu.menu_id == menu_in.id))
    else:
        result = await session.scalars(select(Submenu).options(joinedload(Submenu.dishes))
                                       .where(Submenu.menu_id == menu_in.id, Submenu.id == submenu_in.id))
    for r in result.unique():
        submenu = Submenu(
            id = r.id,
            title = r.title,
            description = r.description
        )
        submenu.dishes_count = len(r.dishes)
        submenus.append(submenu)
    return list(submenus)

async def create_submenu(session: AsyncSession, menu_in: Menu, submenu_in: SubmenuCreate) -> Submenu:
    submenu = Submenu(
        title = submenu_in.title,
        description = submenu_in.description,
        menu_id = menu_in.id
    )
    session.add(submenu)
    await session.commit()
    return submenu

async def update_submenu(session: AsyncSession, 
                      submenu: Submenu, submenu_update: SubmenuUpdate | SubmenuUpdatePartial,
                      partial: bool = False) -> Submenu:
    for key, value in submenu_update.model_dump(exclude_unset=partial).items():
        setattr(submenu, key, value)
    await session.commit()
    return submenu

async def delete_submenu(session: AsyncSession, submenu: Submenu) -> None:
    await session.delete(submenu)
    await session.commit()
    