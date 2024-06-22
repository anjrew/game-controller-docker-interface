# 🎮 Game Controller Rest Interface Project

## Overview

This project is designed to interface with a game controller,
enabling the detection and utilization of controller inputs within a Python application.
Leveraging technologies such as Pygame and Docker,
it provides a robust setup for developing applications that respond to game controller inputs.

### Features

- Detects game controller input using Pygame.
- Dockerized environment for consistent development and testing.
- Real-time input handling and event processing.

## Prerequisites

- Python 3.11 or later.
- Docker and Docker Compose.
- A game controller compatible with standard input libraries.

## 🚀 Getting Started

1. [Git clone](https://git-scm.com/docs/git-clone) or download this repository to your computer.
2. [Setup your development environment](./docs/setting_up_the_environment.md).

## Installation

### Setting Up the Docker Container

1. **Build the Docker Image:**

```bash
docker-compose build
```

## Run the Docker Container

``` bash
docker-compose up
```

## Running the Application

Access the Docker Container:

```bash
docker exec -it [container_name] bash
```

## Run the Script

```bash
python main.py
```

## Usage

The main application can be started with the following command:

```bash
python api/main.py
```

This script initializes the game controller and listens for input events, printing them to the console.
Troubleshooting

Controller Not Detected: Ensure the controller is correctly plugged in and recognized by your host system.
Permission Issues: Make sure the Docker container is running with appropriate permissions to access input devices.

## Environment Variable Feature

The application supports an optional environment variable INFO.
When set, this variable's value is included in the output response as an info property.
This feature allows for dynamic inclusion of additional information in the application's responses.
Setting the INFO Environment Variable

Before running the application, set the info environment variable:

```bash
export INFO="Your custom information here"
```
