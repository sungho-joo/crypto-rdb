"""Main function initializing fastapi app"""

import sys
from typing import Final

from fastapi import FastAPI

from db.database import Database
from src.stat import controller as stat_controller

def create_app() -> FastAPI:
    """Create and do initial configuration of fastapi app"""

#    db = Database()
    # try:
    #     db.create_database()
    # except Exception:  # pylint: disable=broad-except
    #     sys.exit(1)

    app_ = FastAPI()

    # Add routers
    app_.include_router(stat_controller.router)
    # Overide exception handlers

    # Override default class method

    return app_


app = create_app()
