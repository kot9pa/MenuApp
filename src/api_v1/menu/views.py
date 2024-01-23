from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import Menu, MenuView, MenuCreate, MenuUpdate, MenuUpdatePartial
from database import db_helper

router = APIRouter(prefix="/menus", tags=["Menu"])

# Dependencies
async def menu_by_id(
    menu_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> Menu:

    menu = await crud.get_menu(session=session, menu_id=menu_id)
    if menu is not None:
        return menu

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Menu {menu_id} not found!",
    )

@router.get("/", response_model=list[MenuView])
async def get_menus(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_menus(session=session)

@router.get("/{menu_id}/", response_model=Menu)
async def get_menu(menu: Menu = Depends(menu_by_id)):
    return menu

@router.post("/", response_model=Menu, status_code=status.HTTP_201_CREATED)
async def create_menu(
    menu_in: MenuCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_menu(session=session, menu_in=menu_in)

@router.put("/{menu_id}/")
async def update_menu(
    menu_update: MenuUpdate,
    menu: Menu = Depends(menu_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_menu(
        session=session,
        menu=menu,
        menu_update=menu_update,
    )

@router.patch("/{menu_id}/")
async def update_menu_partial(
    menu_update: MenuUpdatePartial,
    menu: Menu = Depends(menu_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_menu(
        session=session,
        menu=menu,
        menu_update=menu_update,
        partial=True,
    )

@router.delete("/{menu_id}/")
async def delete_menu(
    menu: Menu = Depends(menu_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_menu(session=session, menu=menu)

