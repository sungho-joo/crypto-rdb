# -*- coding: utf-8 -*-

"""
API functions based on FastAPI

Author:
    Name: Sungho Joo
    Email: triangle124@gmail.com
"""

from typing import List, Optional

from pydantic import BaseModel


class TickersList(BaseModel):
    """DTO for a Ticker."""

    ticker_list: List[str]


class TickerDataIn(BaseModel):
    """DTO for a scrape data"""

    ticker_list: List[str]
    stats: Optional[str] = None


class TickerDataOut(BaseModel):
    """DTO for a scrape data"""

    ticker: str
    pid: Optional[int]


class TickerDataListOut(BaseModel):
    """DTO for a scrape data"""

    ticker_list: List[TickerDataOut]
