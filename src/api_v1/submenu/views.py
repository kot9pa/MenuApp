from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import Submenu, SubmenuView, SubmenuCreate, SubmenuUpdate, SubmenuUpdatePartial
from api_v1.menu.schemas import Menu
from dependencies import submenu_by_id, menu_by_id
from database import db_helper


router = APIRouter(prefix="/menus/{menu_id}/submenus", tags=["Submenu"])

@router.get("/", response_model=list[SubmenuView])
async def get_submenus(
    menu_in: Menu = Depends(menu_by_id), 
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_submenu_with_counts(session=session, menu_in=menu_in)

@router.get("/{submenu_id}/", response_model=SubmenuView)
async def get_submenu(    
    submenu_in: Submenu = Depends(submenu_by_id),
    menu_in: Menu = Depends(menu_by_id), 
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    result = await crud.get_submenu_with_counts(session=session, menu_in=menu_in, submenu_in=submenu_in)
    return result[0]

@router.post("/", response_model=Submenu, status_code=status.HTTP_201_CREATED)
async def create_submenu(    
    submenu_in: SubmenuCreate,
    menu_in: Menu = Depends(menu_by_id), 
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_submenu(session=session, menu_in=menu_in, submenu_in=submenu_in)

@router.put("/{submenu_id}/")
async def update_submenu(
    submenu_update: SubmenuUpdate,
    submenu: Submenu = Depends(submenu_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_submenu(
        session=session,
        submenu=submenu,
        submenu_update=submenu_update,
    )

@router.patch("/{submenu_id}/")
async def update_submenu_partial(
    submenu_update: SubmenuUpdatePartial,
    submenu: Submenu = Depends(submenu_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_submenu(
        session=session,
        submenu=submenu,
        submenu_update=submenu_update,
        partial=True,
    )

@router.delete("/{submenu_id}/")
async def delete_submenu(
    submenu: Submenu = Depends(submenu_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_submenu(session=session, submenu=submenu)
