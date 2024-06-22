import logging
import os
from typing import Any, Dict

import pygame
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from game_controllers.controller_input import ControllerInput

LOGGER = logging.getLogger(__name__)

app = FastAPI(
    title="Turtle Beach Recon Controller Input API",
    description="API to get controller input for speed and steering",
    version="0.1.0",
)

X_BUTTON_INDEX = 2
A_BUTTON_INDEX = 0
LEFT_STICK_X_AXIS = 0
RIGHT_TRIGGER_AXIS = 5
joystick = None

# Initialize Pygame and Joystick
pygame.init()
pygame.joystick.init()


def initialize_joystick() -> None:
    """
    Initializes the first joystick if any are connected.
    """
    global joystick
    joystick_count = pygame.joystick.get_count()
    LOGGER.info(f"Number of joysticks detected: {joystick_count}")
    if joystick_count > 0:
        joystick = pygame.joystick.Joystick(0)
        LOGGER.info(f"Found Joystick: {joystick.get_name()}")
        joystick.init()
        LOGGER.info("Joystick initialized.")
    else:
        print("No game controller detected.")


initialize_joystick()


def get_speed_and_steering() -> Dict[str, Any]:
    """
    Retrieves the current positions of the left stick X-axis and the right trigger axis.

    Returns:
        A dictionary containing the positions of the left stick X-axis and the right trigger axis.
    """
    if not joystick:
        raise HTTPException(status_code=404, detail="Joystick not initialized")

    pygame.event.pump()  # Process event queue
    return {
        "left_stick_x_axis": joystick.get_axis(LEFT_STICK_X_AXIS),
        "right_trigger_axis": joystick.get_axis(RIGHT_TRIGGER_AXIS),
        "x_button_pressed": joystick.get_button(X_BUTTON_INDEX),
        "a_button_pressed": joystick.get_button(A_BUTTON_INDEX),
    }


@app.get("/controller-input")
async def controller_input() -> ControllerInput:
    """
    Endpoint to get the current controller input for speed and steering.

    Returns:
        JSON response containing the current positions of the left stick X-axis and the right trigger axis.
    """
    response_data = get_speed_and_steering()

    info_env_var = os.getenv("INFO")
    if info_env_var is not None:
        response_data["info"] = info_env_var

    return ControllerInput.model_validate(response_data)


@app.get("/")
async def redirect_to_docs() -> RedirectResponse:
    """
    Redirects to docs
    """
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
