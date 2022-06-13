# -*- coding: utf-8 -*-
# mypy: ignore-errors

"""
API functions based on FastAPI

Author:
    Name: Sungho Joo
    Email: triangle124@gmail.com
"""

import os

import pyupbit
from fastapi import APIRouter

from upbit.schema import ScrapeDataIn, TickersGetOut
from upbit.utils import check_market_code_valid, run_cmd

router = APIRouter(prefix="/upbit", tags=["upbit"], responses={404: {"description": "Not found"}})


@router.get("/tickers", response_model=TickersGetOut)
def get_tickers() -> TickersGetOut:
    """Get all tickers"""
    tickers = pyupbit.get_tickers()
    return TickersGetOut(ticker_list=tickers)


@router.post("/tickers", response_model=None)
def scrape_data(
    request_body: ScrapeDataIn,
) -> None:
    """Get price for given market code"""
    market_code = request_body.market_code
    stat = request_body.stat

    check_market_code_valid(market_code)

    # TBD: when stat is given
    if stat:
        return

    for market_code in market_code:
        cmd = f"PYTHONPATH=/usr/app/src/ python upbit/websocket.py --market-code {market_code}"
        pid = run_cmd(cmd)

    # TBD: add pid to DB and remove pid when necessary
    os.kill(pid, 9)
