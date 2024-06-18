import time
import pygame


def initialize_controller():
    pygame.init()
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()

    if joystick_count == 0:
        print("No game controller detected.")
        return None

    # Use the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    return joystick


def get_controller_input(joystick int):
    pygame.event.pump()  # Process event queue

    # Read joystick axes, buttons, and hats
    axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
    hats = [joystick.get_hat(i) for i in range(joystick.get_numhats())]

    return axes, buttons, hats


def main():
    joystick = initialize_controller()

    if not joystick:
        return

    print(f"Controller connected: {joystick.get_name()}")

    try:
        while True:
            axes, buttons, hats = get_controller_input(joystick)
            # print(f"Axes: {axes}")
            print(f"Buttons: {buttons}")
            # print(f"Hats: {hats}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
