# api/containers.py
from dependency_injector import containers, providers

from game_controllers.services.joystick_service import JoystickService
from game_controllers.services.pygame_connector import PyGameConnector


class DependencyContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(modules=[".routers.controllers"])
    py_game_connector = providers.Factory(PyGameConnector)
    joystick_service = providers.Factory(
        JoystickService, pygame_connector=py_game_connector
    )
