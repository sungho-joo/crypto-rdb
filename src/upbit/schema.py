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

    market_codes: List[str]
    stat: str = ""


class TickerDataOut(BaseModel):
    """DTO for a scrape data"""

    market_code: str
    pid: Optional[int]


class TickerDataListOut(BaseModel):
    """DTO for a scrape data"""

    ticker_list: List[TickerDataOut]
