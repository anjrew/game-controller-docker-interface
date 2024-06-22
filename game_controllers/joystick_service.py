from typing import Any, Dict, List

from game_controllers.pygame_connector import PyGameConnector


class JoystickService:

    def __init__(self, pygame_connector: PyGameConnector) -> None:
        self.pygame_connector = pygame_connector

    def get_joysticks_details(self) -> List[Dict[str, Any]]:
        joysticks = []
        joystick_count = self.pygame_connector.get_joystick_count()
        for i in range(joystick_count):
            joystick = self.pygame_connector.create_joystick(i)
            joystick.init()
            joysticks.append(
                {
                    "id": i,
                    "name": joystick.get_name(),
                    "num_axes": joystick.get_numaxes(),
                    "num_buttons": joystick.get_numbuttons(),
                    "num_hats": joystick.get_numhats(),
                    "num_balls": joystick.get_numballs(),
                }
            )
        return joysticks
