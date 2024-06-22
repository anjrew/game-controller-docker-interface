import logging

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.containers import DependencyContainer
from api.docs import CONTROLLERS_PATH
from api.routers.controllers import router as controllers_router

LOGGER = logging.getLogger(__name__)

app = FastAPI(
    title="Turtle Beach Recon Controller Input API",
    description="API to get controller input for speed and steering",
    version="0.1.0",
)


app.include_router(
    controllers_router,
    prefix=f"/{CONTROLLERS_PATH}",
)


@app.get("/")
async def redirect_to_docs() -> RedirectResponse:
    """
    Redirects to docs
    """
    return RedirectResponse(url="/docs")


container = DependencyContainer()
container.wire(modules=[__name__])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
