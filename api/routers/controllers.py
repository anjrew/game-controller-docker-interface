import logging
from typing import List

from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends

from api.containers import DependencyContainer
from game_controllers.models.joystick_details import JoystickDetails
from game_controllers.services.joystick_service import JoystickService

router = APIRouter()

LOGGER = logging.getLogger(__name__)


@router.get("/controller/list")
async def list_controllers(
    joystick_service: JoystickService = Depends(
        Provide[DependencyContainer.joystick_service]
    ),
) -> List[JoystickDetails]:
    LOGGER.info("List controllers")
    return joystick_service.get_joysticks_details()
