"""Main function initializing fastapi app"""

import stat.controller as stat_controller

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create and do initial configuration of fastapi app"""

    app_ = FastAPI()

    # Add routers
    app_.include_router(stat_controller.router)

    return app_


app = create_app()
