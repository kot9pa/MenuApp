from typing import Annotated
from fastapi import HTTPException, Path, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.menu import crud as crud_menu
from api_v1.submenu import crud as crud_submenu
from api_v1.menu.schemas import Menu
from api_v1.submenu.schemas import Submenu
from database import db_helper


async def menu_by_id(
    menu_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> Menu:

    menu = await crud_menu.get_menu(session=session, menu_id=menu_id)
    if menu is not None:
        return menu

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"menu not found",
    )

async def submenu_by_id(
    menu_id: Annotated[int, Path],
    submenu_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> Submenu:

    submenu = await crud_submenu.get_submenu(session=session, menu_id=menu_id, submenu_id=submenu_id)
    if submenu is not None:
        return submenu

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"submenu not found",
    )
