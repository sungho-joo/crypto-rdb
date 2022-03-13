"""Main function initializing fastapi app"""

import sys
from typing import Final

from fastapi import FastAPI

from src.db.database import Database

API_VERSION_1: Final = "/v1"


def create_app() -> FastAPI:
    """Create and do initial configuration of fastapi app"""

    db = Database()
    try:
        db.create_database()
    except Exception:  # pylint: disable=broad-except
        sys.exit(1)

    app_ = FastAPI()

    # Add routers
    # app_.include_router(project_controller.router, prefix=API_VERSION_1)
    # app_.include_router(user_controller.router, prefix=API_VERSION_1)
    # app_.include_router(model_controller.router, prefix=API_VERSION_1)
    # app_.include_router(data_source_controller.router, prefix=API_VERSION_1)
    # Overide exception handlers

    # Override default class method

    return app_


app = create_app()
