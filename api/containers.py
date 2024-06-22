"""Containers module."""

from dependency_injector import containers, providers

from game_controllers.services.joystick_service import JoystickService
from game_controllers.services.pygame_connector import PyGameConnector


class DependencyContainer(containers.DeclarativeContainer):

    # Get all the configuration values from the environment
    config = providers.Configuration()

    py_game = providers.Singleton[PyGameConnector](PyGameConnector)
    joystick_service = providers.Singleton[JoystickService](
        JoystickService, pygame_connector=py_game
    )
