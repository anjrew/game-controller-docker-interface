from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from typing import List


@dataclass
class StickState:
    horizontal_right: float
    "If positive the stick is in the right position, else left"
    vertical_down: float
    "If positive the stick is in the down position, else up"


@dataclass
class ControllerAxesState:
    left_stick: StickState
    right_stick: StickState
    left_analog_trigger: float
    right_analog_trigger: float


@dataclass
class ControllerDPadState:
    horizontal_right: int
    """
    If positive, the D-pad is pressed right,
    if negative, the D-pad is pressed left.
    If 0, the D-pad is not pressed
    """
    vertical_up: int
    """
    If positive, the D-pad is pressed up,
    if negative, the D-pad is pressed down.
    If 0, the D-pad is not pressed"""

    def get_active(self) -> List[str]:
        return [field.name for field in fields(self) if getattr(self, field.name) != 0]


class ControllerButtonPressedState(ABC):
    @abstractmethod
    def get_pressed_buttons(self) -> List[str]:
        pass
