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
    market_code: str
    value: Dict[int, Any]


class StatsGetOut(BaseModel):
    """DTO for stats"""

    stats: List[StatGetOut]


class StatGetIn(BaseModel):
    """DTO for Price in"""

    market_code: List[str]
    start_date: str
    end_date: str

    class Config:
        """Schema configuration"""

        schema_extra = {
            "example": {
                "market_code": ["KRW-BTC"],
                "start_date": "2022-03-18",
                "end_date": "2022-04-19",
            }
        }
