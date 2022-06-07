"""Main function initializing fastapi app"""

import os
from pathlib import Path

from fastapi import FastAPI

import crypto.stat.controller as stat_controller

main_path = Path(os.path.abspath(__file__))
os.chdir(main_path.parent)


def create_app() -> FastAPI:
    """Create and do initial configuration of fastapi app"""

    app_ = FastAPI()

    # Add routers
    app_.include_router(stat_controller.router)

    return app_


app = create_app()
