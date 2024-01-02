from fastapi import FastAPI, HTTPException
import pygame
from typing import Dict

app = FastAPI(
    title="Turtle Beach Recon Controller Input API", 
    description="API to get controller input for speed and steering", 
    version="0.1.0"
)

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
    if joystick_count > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    else:
        print("No game controller detected.")

initialize_joystick()

def get_speed_and_steering() -> Dict[str, float]:
    """
    Retrieves the current positions of the left stick X-axis and the right trigger axis.

    Returns:
        A dictionary containing the positions of the left stick X-axis and the right trigger axis.
    """
    if not joystick:
        raise HTTPException(status_code=404, detail="Joystick not initialized")
    
    pygame.event.pump()  # Process event queue
    return {
        'left_stick_x_axis': joystick.get_axis(LEFT_STICK_X_AXIS), 
        'right_trigger_axis': joystick.get_axis(RIGHT_TRIGGER_AXIS)
    }

@app.get("/controller-input", response_model=Dict[str, float])
async def controller_input() -> Dict[str, float]:
    """
    Endpoint to get the current controller input for speed and steering.

    Returns:
        JSON response containing the current positions of the left stick X-axis and the right trigger axis.
    """
    return get_speed_and_steering()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
