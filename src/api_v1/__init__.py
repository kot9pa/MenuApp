from fastapi import APIRouter

from api_v1.menu.views import router as menu_router
from api_v1.submenu.views import router as submenu_router
from api_v1.dish.views import router as dish_router

internal_router = APIRouter()
internal_router.include_router(router=menu_router)
internal_router.include_router(router=submenu_router)
internal_router.include_router(router=dish_router)