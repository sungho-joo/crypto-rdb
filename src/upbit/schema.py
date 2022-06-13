# -*- coding: utf-8 -*-

"""
API functions based on FastAPI

Author:
    Name: Sungho Joo
    Email: triangle124@gmail.com
"""

from typing import List

from pydantic import BaseModel


class TickersGetOut(BaseModel):
    """DTO for a Ticker."""

    ticker_list: List[str]


class ScrapeDataIn(BaseModel):
    """DTO for a scrape data"""

    market_code: List[str]
    stat: str
