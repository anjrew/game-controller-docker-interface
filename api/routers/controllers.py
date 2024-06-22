import logging
from typing import List, Optional

from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import DependencyContainer
from game_controllers.models.controller_state import ControllerState
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


@router.post("/controller/{joystick_id}/initialize")
async def initialize_controller(
    joystick_id: int,
    controller_type: str,
    platform: Optional[str] = None,
    joystick_service: JoystickService = Depends(
        Provide[DependencyContainer.joystick_service]
    ),
) -> str:
    LOGGER.info(f"Initialize joystick {joystick_id}")
    try:
        joystick_service.create_joystick(joystick_id, controller_type, platform)
        return f"Joystick {joystick_id} initialized"
    except Exception as e:
        LOGGER.error(f"Failed to initialize joystick {joystick_id}: {e}")
        raise HTTPException(status_code=500, detail="Initialization failed")


@router.get("/controller/{joystick_id}/state")
async def get_controller_state(
    joystick_id: int,
    joystick_service: JoystickService = Depends(
        Provide[DependencyContainer.joystick_service]
    ),
) -> ControllerState:
    LOGGER.info(f"Get state of joystick {joystick_id}")
    try:
        return joystick_service.get_joystick_state(joystick_id)
    except KeyError as e:
        LOGGER.error(
            f"Failed to find joystick with id{joystick_id}: {e}", exc_info=True
        )
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        LOGGER.error(
            f"Failed to get value of joystick {joystick_id}: {e}", exc_info=True
        )
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        LOGGER.error(
            f"Failed to get state of joystick {joystick_id}: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail="Failed to get joystick state")


@router.delete("/controller/{joystick_id}/remove")
async def remove_controller(
    joystick_id: int,
    joystick_service: JoystickService = Depends(
        Provide[DependencyContainer.joystick_service]
    ),
) -> str:
    LOGGER.info(f"Remove joystick {joystick_id}")
    try:
        joystick_service.remove_joystick(joystick_id)
        return f"Joystick {joystick_id} removed"
    except ValueError as e:
        LOGGER.error(f"Failed to remove joystick {joystick_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        LOGGER.error(f"Failed to remove joystick {joystick_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to remove joystick")
