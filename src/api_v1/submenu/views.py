from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.menu.schemas import Menu

from . import crud
from .schemas import Submenu, SubmenuCreate, SubmenuUpdate, SubmenuUpdatePartial
from database import db_helper

router = APIRouter(prefix="/menus/{menu_id}/submenus", tags=["Submenu"])

# Dependencies
async def submenu_by_id(
    menu_id: Annotated[int, Path],
    submenu_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> Submenu:

    submenu = await crud.get_submenu(session=session, menu_id=menu_id, submenu_id=submenu_id)
    if submenu is not None:
        return submenu

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Submenu {submenu_id} not found!",
    )

@router.get("/", response_model=list[Submenu])
async def get_submenus(
    menu_id: Annotated[int, Path], 
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_submenus(session=session, menu_id=menu_id)

@router.get("/{submenu_id}/", response_model=Submenu)
async def get_submenu(submenu: Submenu = Depends(submenu_by_id)):
    return submenu

@router.post("/", response_model=Submenu, status_code=status.HTTP_201_CREATED)
async def create_submenu(
    menu_id: Annotated[int, Path],
    submenu_in: SubmenuCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_submenu(session=session, menu_id=menu_id, submenu_in=submenu_in)

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
