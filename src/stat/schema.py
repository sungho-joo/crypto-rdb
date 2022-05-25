# -*- coding: utf-8 -*-

"""
API functions based on FastAPI

Author:
    Name: Sungho Joo
    Email: triangle124@gmail.com
"""

from typing import Any, Dict, List

from pydantic import BaseModel


class TickersGetOut(BaseModel):
    """DTO for a Ticker."""

    ticker_list: List[str]


class StatGetOut(BaseModel):
    """DTO for a stat"""

    stat_name: str
    value: Dict[int, Any]


class StatsGetOut(BaseModel):
    """DTO for stats"""

    stats: List[StatGetOut]
