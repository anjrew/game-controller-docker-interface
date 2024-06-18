from typing import Optional
from pydantic import BaseModel


class ControllerInput(BaseModel):
    left_stick_x_axis: float
    right_trigger_axis: float
    x_button_pressed: bool
    a_button_pressed: bool
    info: Optional[str] = None
    