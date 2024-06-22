import logging
from typing import Dict, List, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import DependencyContainer
from api.docs import CONTROLLERS_PATH
from api.models.initialize_controller_request import InitializeControllerRequest
from game_controllers.models.controller_state import ControllerState
from game_controllers.models.joystick_details import JoystickDetails
from game_controllers.services.joystick_service import JoystickService

LOGGER = logging.getLogger(__name__)

router = APIRouter(prefix=f"/{CONTROLLERS_PATH}", tags=[CONTROLLERS_PATH.capitalize()])


@router.get("/connected/list")
@inject
async def list_connected_controllers(
    joystick_service: JoystickService = Depends(
        Provide[DependencyContainer.joystick_service]
    ),
) -> List[JoystickDetails]:
    return joystick_service.get_joysticks_details()


@router.get("/compatible/list")
@inject
async def list_compatible_controllers(
    joystick_service: JoystickService = Depends(
        Provide[DependencyContainer.joystick_service]
    ),
) -> Dict[str, List[str]]:
    return joystick_service.get_compatible_joysticks()


@router.post("/{joystick_id}/initialize")
@inject
async def initialize_controller(
    joystick_id: int,
    request: InitializeControllerRequest,
    joystick_service: JoystickService = Depends(
        Provide[DependencyContainer.joystick_service]
    ),
) -> str:
    LOGGER.info(
        f"Initialize joystick {joystick_id} with type {request.controller_type}"
    )
    try:
        joystick_service.create_joystick(
            joystick_id, request.controller_type, request.platform
        )
        return f"Joystick {joystick_id} initialized"
    except Exception as e:
        LOGGER.error(f"Failed to initialize joystick {joystick_id}: {e}")
        raise HTTPException(status_code=500, detail="Initialization failed")


@router.get("/{joystick_id}/state", response_model=None)
@inject
async def get_controller_state(
    joystick_id: int,
    joystick_service: JoystickService = Depends(
        Provide[DependencyContainer.joystick_service]
    ),
) -> ControllerState:
    """
    This endpoint returns the state of the joystick with the given ID
    Args:
        joystick_id (int): The ID of the joystick to get the state of

    Returns:
        Any: The Caller should know what to expect from the return value as it depends on the controller type
    """
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


@router.delete("/{joystick_id}/remove")
@inject
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
