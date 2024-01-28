from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import Dish, DishCreate, DishUpdate, DishUpdatePartial
from database import db_helper

router = APIRouter(prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes", tags=["Dish"])

# Dependencies
async def dish_by_id(
    submenu_id: Annotated[int, Path],
    dish_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)) -> Dish:

    dish = await crud.get_dish(session=session, submenu_id=submenu_id, dish_id=dish_id)
    if dish is not None:
        return dish

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"dish not found",
    )

@router.get("/", response_model=list[Dish])
async def get_dishes(
    submenu_id: Annotated[int, Path], 
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_dishes(session=session, submenu_id=submenu_id)

@router.get("/{dish_id}/", response_model=Dish)
async def get_dish(dish: Dish = Depends(dish_by_id)):
    return dish

@router.post("/", response_model=Dish, status_code=status.HTTP_201_CREATED)
async def create_dish(
    submenu_id: Annotated[int, Path],
    dish_in: DishCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_dish(session=session, submenu_id=submenu_id, dish_in=dish_in)

@router.put("/{dish_id}/")
async def update_dish(
    dish_update: DishUpdate,
    dish: Dish = Depends(dish_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_dish(
        session=session,
        dish=dish,
        dish_update=dish_update,
    )

@router.patch("/{dish_id}/")
async def update_dish_partial(
    dish_update: DishUpdatePartial,
    dish: Dish = Depends(dish_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_dish(
        session=session,
        dish=dish,
        dish_update=dish_update,
        partial=True,
    )

@router.delete("/{dish_id}/")
async def delete_dish(
    dish: Dish = Depends(dish_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_dish(session=session, dish=dish)
