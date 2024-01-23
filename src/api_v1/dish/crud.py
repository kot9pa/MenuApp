from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Dish
from .schemas import DishCreate, DishUpdate, DishUpdatePartial


async def get_dishes(session: AsyncSession, submenu_id: int) -> list[Dish]:
    stmt = select(Dish).where(Dish.submenu_id == submenu_id)
    result: Result = await session.execute(stmt)
    #dish: Dish | None = await session.scalar(stmt)
    dishes = result.scalars().all()
    return list(dishes)

async def get_dish(session: AsyncSession, submenu_id: int, dish_id: int) -> Dish | None:
    stmt = select(Dish).where(Dish.submenu_id == submenu_id, Dish.id == dish_id)
    return await session.scalar(stmt)

async def create_dish(session: AsyncSession, submenu_id: int, dish_in: DishCreate) -> Dish:
    dish = Dish(
        title = dish_in.title,
        description = dish_in.description,
        price = dish_in.price,
        submenu_id = submenu_id
    )
    session.add(dish)
    await session.commit()
    return dish

async def update_dish(session: AsyncSession, 
                      dish: Dish, dish_update: DishUpdate | DishUpdatePartial,
                      partial: bool = False) -> Dish:
    for key, value in dish_update.model_dump(exclude_unset=partial).items():
        setattr(dish, key, value)
    await session.commit()
    return dish

async def delete_dish(session: AsyncSession, dish: Dish) -> None:
    await session.delete(dish)
    await session.commit()
    