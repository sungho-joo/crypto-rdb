"""Main function initializing fastapi app"""

from fastapi import FastAPI
from src.stat import controller as stat_controller


def create_app() -> FastAPI:
    """Create and do initial configuration of fastapi app"""

    app_ = FastAPI()

    # Add routers
    app_.include_router(stat_controller.router)

    return app_


app = create_app()
