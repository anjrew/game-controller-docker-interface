from abc import ABC, abstractmethod

from game_controllers.models.controller_state import ControllerState


class GameControllerInterface(ABC):
    @abstractmethod
    def get_state(self) -> ControllerState:
        """Gets the current controller state"""

    @abstractmethod
    def dispose(self) -> None:
        """Disposes the controller and its resources"""
