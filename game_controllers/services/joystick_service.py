import logging
import os
from typing import Dict, List, Optional

import pygame

from game_controllers.interfaces.game_controller_interface import (
    ControllerState,
    GameControllerInterface,
)
from game_controllers.joysticks.xbox_controller import XboxPyGameController
from game_controllers.models.joystick_details import JoystickDetails
from game_controllers.services.pygame_connector import PyGameConnector

LOGGER = logging.getLogger(__name__)


class JoystickService:
    "A Stateful service to manage the joysticks connected to the system"

    joysticks: Dict[int, GameControllerInterface] = {}

    def __init__(self, pygame_connector: PyGameConnector) -> None:
        self.pygame_connector = pygame_connector

    def get_joysticks_details(self) -> List[JoystickDetails]:
        """
        Gets the details of all the currently detectable connected joysticks to the system
        """
        joysticks: List[JoystickDetails] = []
        joystick_count = self.pygame_connector.get_joystick_count()
        for i in range(joystick_count):
            joystick = self.pygame_connector.create_joystick(i)
            joystick.init()
            joysticks.append(self.get_joystick_details(joystick))

        return joysticks

    @staticmethod
    def get_joystick_details(joystick: pygame.joystick.JoystickType) -> JoystickDetails:
        return JoystickDetails(
            id=joystick.get_id(),
            name=joystick.get_name(),
            num_axes=joystick.get_numaxes(),
            num_buttons=joystick.get_numbuttons(),
            num_hats=joystick.get_numhats(),
            num_balls=joystick.get_numballs(),
        )

    def get_joystick_state(self, joystick_id: int) -> ControllerState:
        if joystick_id not in self.joysticks:
            raise ValueError(f"Joystick {joystick_id} not initialized")
        joystick = self.joysticks[joystick_id]
        return joystick.get_state()

    def create_joystick(
        self, joystick_id: int, controller: str, platform: Optional[str]
    ) -> None:

        if "xbox_controller" not in controller:
            raise ValueError(f"Controller {controller} not supported")

        self.joysticks[joystick_id] = XboxPyGameController(
            self.pygame_connector, joystick_id, platform
        )

        LOGGER.info(f"Joystick {joystick_id} removed")

    def remove_joystick(self, joystick_id: int) -> None:
        if joystick_id not in self.joysticks:
            raise ValueError(f"Joystick {joystick_id} not initialized")
        joystick = self.joysticks.pop(joystick_id)
        joystick.dispose()
        LOGGER.info(f"Joystick {joystick_id} removed")

    def get_compatible_joysticks(
        self, base_dir: Optional[str] = None
    ) -> Dict[str, List[str]]:
        if base_dir is None:
            base_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "..", "joysticks"
            )
        joysticks: Dict[str, List[str]] = {}
        for root, dirs, _ in os.walk(base_dir):
            for controller_dir in dirs:
                if controller_dir != "__pycache__":
                    joystick_path = os.path.join(root, controller_dir)
                    platforms = [
                        file[:-3]
                        for file in os.listdir(joystick_path)
                        if file.endswith(".py") and file != "__init__.py"
                    ]
                    joysticks[controller_dir] = platforms
        LOGGER.info(f"Available joysticks: {joysticks}")
        return joysticks


# Example usage:
if __name__ == "__main__":
    pygame_connector = PyGameConnector()
    pygame_connector.init_joystick()
    joystick_service = JoystickService(pygame_connector)

    # Get joystick details
    joystick_details = joystick_service.get_joysticks_details()
    for details in joystick_details:
        print(details)

    # Get available joysticks and compatible platforms
    available_joysticks = joystick_service.get_compatible_joysticks()
    for joystick, platforms in available_joysticks.items():
        print(f"Joystick: {joystick}, Platforms: {platforms}")

    pygame_connector.dispose()
