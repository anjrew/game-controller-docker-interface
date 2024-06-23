import argparse
import logging

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.dependencies import DependencyContainer
from api.routers.controllers import router as controllers_router

LOGGER = logging.getLogger(__name__)

app = FastAPI(
    title="Game Controller REST API",
    description="REST API to query the state of game controllers connected to the system",
    version="0.1.0",
)

container = DependencyContainer()

app.include_router(
    controllers_router,
    prefix="/api/v1",
)


@app.get("/", tags=["Root"])
async def redirect_to_docs() -> RedirectResponse:
    """
    Redirects to docs
    """
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    parser = argparse.ArgumentParser(
        description="Run the Game Controller REST API server"
    )
    parser.add_argument(
        "--log-level",
        default="error",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Set the logging level",
    )
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    args = parser.parse_args()

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=args.reload,
        log_level=args.log_level,
    )
