from dataclasses import asdict, dataclass
from typing import Any, Dict

from game_controllers.models.controller_elements import (
    ControllerAxesState,
    ControllerButtonPressedState,
    ControllerDPadState,
)


@dataclass
class ControllerState:
    """
    This state represents the desired state for the controller.
    """

    # The axis control range
    AXIS_MIN_VAL = -1
    AXIS_MAX_VAL = 1

    axes: ControllerAxesState
    buttons: ControllerButtonPressedState
    d_pad: ControllerDPadState

    def __post_init__(self):
        self.validate_direction(
            "axes.left_stick.horizontal", self.axes.left_stick.horizontal_right
        )
        self.validate_direction(
            "axes.left_stick.vertical", self.axes.left_stick.vertical_down
        )
        self.validate_direction(
            "axes.right_stick.horizontal", self.axes.right_stick.horizontal_right
        )
        self.validate_direction(
            "axes.right_stick.vertical", self.axes.right_stick.vertical_down
        )
        self.validate_direction(
            "axes.left_analog_trigger", self.axes.left_analog_trigger
        )
        self.validate_direction(
            "axes.right_analog_trigger", self.axes.right_analog_trigger
        )

    def validate_direction(self, attribute_name: str, value: float):
        if not isinstance(value, float):
            raise ValueError(
                f"{attribute_name} value needs to be an float. Got {type(value)}"
            )
        if not (self.AXIS_MIN_VAL <= value <= self.AXIS_MAX_VAL):
            raise ValueError(
                f"Value {value} for attribute '{attribute_name}' "
                f"is not in the range [{self.AXIS_MIN_VAL}, {self.AXIS_MAX_VAL}]"
            )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
