from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Submenu
from .schemas import SubmenuCreate, SubmenuUpdate, SubmenuUpdatePartial


async def get_submenus(session: AsyncSession, menu_id: int) -> list[Submenu]:
    stmt = select(Submenu).where(Submenu.menu_id == menu_id)
    result: Result = await session.execute(stmt)
    #submenu: Submenu | None = await session.scalar(stmt)
    submenus = result.scalars().all()
    return list(submenus)

async def get_submenu(session: AsyncSession, menu_id: int, submenu_id: int) -> Submenu | None:
    stmt = select(Submenu).where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
    return await session.scalar(stmt)

async def create_submenu(session: AsyncSession, menu_id: int, submenu_in: SubmenuCreate) -> Submenu:
    submenu = Submenu(
        title = submenu_in.title,
        description = submenu_in.description,
        menu_id = menu_id
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
    