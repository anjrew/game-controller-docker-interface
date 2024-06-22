from typing_extensions import TypedDict


class JoystickDetails(TypedDict):
    """Information about a joystick or game controller"""

    id: int
    name: str
    num_axes: int
    num_buttons: int
    num_hats: int
    num_balls: int
