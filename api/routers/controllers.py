import logging

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from api.containers import DependencyContainer

router = APIRouter()

LOGGER = logging.getLogger(__name__)


@router.get("/controller/list")
async def list_controllers(
    default_query: str = Depends(Provide[DependencyContainer.py_game.]),
):
    LOGGER.info("List controllers")
    return {"controllers": ["controller1", "controller2"]}
