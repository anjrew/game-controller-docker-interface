"""Containers module."""

from dependency_injector import containers, providers

from game_controllers.pygame_connector import PyGameConnector


class DependencyContainer(containers.DeclarativeContainer):

    # Get all the configuration values from the environment
    config = providers.Configuration()

    py_game = providers.Singleton[PyGameConnector](PyGameConnector)
