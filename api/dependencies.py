# api/containers.py
from dependency_injector import containers, providers

from game_controllers.services.joystick_service import JoystickService
from game_controllers.services.pygame_connector import PyGameConnector


class DependencyContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    relative_router_controller_path = ".routers.controllers"
    wiring_config = containers.WiringConfiguration(
        modules=[relative_router_controller_path]
    )
    py_game_connector = providers.Factory(PyGameConnector)
    joystick_service = providers.Factory(
        JoystickService, pygame_connector=py_game_connector
    )
