from enum import Enum


class SystemPlatform(Enum):
    WINDOWS = "win"
    LINUX = "linux"
    MAC = "darwin"

    @classmethod
    def detect(cls):
        import sys

        if "darwin" in sys.platform:
            return cls.MAC
        elif sys.platform.startswith("linux"):
            return cls.LINUX
        elif sys.platform.startswith("win"):
            return cls.WINDOWS
        else:
            raise ValueError(f"Unknown platform {sys.platform}")
