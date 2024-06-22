from typing import Optional

from pydantic import BaseModel


class InitializeControllerRequest(BaseModel):
    controller_type: str
    platform: Optional[str] = None
