"""
This module contains the class that select the correct implementation of the xbox controller based on the platform.
It has the implementation of a General "Xbox Wireless" controller.
https://www.amazon.de/-/en/gp/product/B07SDFLVKD/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1
.. image:: docs/images/xbox_pad.jpeg
   :alt: General Xbox Wireless Controller
   :width: 400px
   :align: center
It provides classes for handling the controller's axes, buttons, and D-pad state.
The `Controller` abstract base class defines the interface for getting the current controller state.
The `XboxPyGameJoystick` class is a concrete implementation of the `Controller` interface using the PyGame library.
"""

import logging
import sys
import time
from typing import Dict, Optional

from game_controllers.enums.system_platforms import SystemPlatform
from game_controllers.interfaces.game_controller_interface import (
    GameControllerInterface,
)
from game_controllers.joysticks.xbox_controller.linux import LinuxXboxPyGameJoystick
from game_controllers.joysticks.xbox_controller.mac import MacXboxPyGameJoystick
from game_controllers.joysticks.xbox_controller.windows import WindowsXboxPyGameJoystick
from game_controllers.models.controller_state import ControllerState
from game_controllers.services.pygame_connector import PyGameConnector

_LOGGER = logging.getLogger(__name__)


class XboxPyGameController(GameControllerInterface):
    """
    The controller works on two main principles
        - That the axes act like a stream of data and are constant
        - The buttons are event based as in only when a button is pressed is the button acknowledged.
            The release of the button is not acknowledged directly but can be inferred
    """

    platform_controller: GameControllerInterface

    def __init__(
        self,
        pygame_connector: PyGameConnector,
        joystick_id: int = 0,
        platform: Optional[str] = None,
    ):
        platform = platform or sys.platform
        if platform == SystemPlatform.MAC:
            self.platform_controller = MacXboxPyGameJoystick(
                pygame_connector, joystick_id
            )
        elif platform == SystemPlatform.LINUX:
            self.platform_controller = LinuxXboxPyGameJoystick(
                pygame_connector, joystick_id
            )
        elif platform == SystemPlatform.WINDOWS:
            self.platform_controller = WindowsXboxPyGameJoystick(
                pygame_connector, joystick_id
            )
        else:
            raise ValueError(
                f"Unknown platform {platform}. Cannot create {self.__class__.__name__}."
                f"No implementation for this platform: {platform}"
            )

    def get_state(self) -> ControllerState:
        return self.platform_controller.get_state()

    def dispose(self) -> None:
        self.platform_controller.dispose()


if __name__ == "__main__":
    import os

    log_level = logging.INFO
    logging.basicConfig(level=log_level)
    _LOGGER.setLevel(log_level)
    pygame_connector = PyGameConnector()
    pygame_joystick = XboxPyGameController(pygame_connector)

    def print_state(state_dict: Dict[str, str], indent: str = ""):
        for k, v in state_dict.items():
            if isinstance(v, dict):
                print(f"{indent}{k}:")
                print_state(v, indent + "  ")
            else:
                print(f"{indent}{k}: {v}")

    while True:
        os.system("cls" if os.name == "nt" else "clear")  # Clear the console
        print("\033[1;1H")  # Move the cursor to the top-left corner

        state = pygame_joystick.get_state()
        print(f"Current state on platform {sys.platform} :")
        dict_state = state.to_dict()

        print_state(dict_state)

        time.sleep(0.1)
