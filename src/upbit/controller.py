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

from upbit.repository import UpbitDBRepository
from upbit.schema import TickerDataIn, TickersList
from upbit.utils import check_market_code_valid, run_cmd

router = APIRouter(prefix="/upbit", tags=["upbit"], responses={404: {"description": "Not found"}})

repository = UpbitDBRepository()


@router.get("/tickers", response_model=TickersList)
def get_tickers() -> TickersList:
    """Get all tickers"""
    tickers = pyupbit.get_tickers()
    return TickersList(ticker_list=tickers)


@router.get("/tickers/active", response_model=TickersList)
def get_active_tickers() -> TickersList:
    """Get all active tickers"""
    active_tickers = repository.get_active_tickers()
    return TickersList(ticker_list=active_tickers)


@router.post("/tickers", response_model=None)
def turnon_data(
    request_body: TickerDataIn,
) -> None:
    """Start websocket scraping for given market codes"""
    market_code = request_body.market_code
    stat = request_body.stat

    check_market_code_valid(market_code)

    # TBD: when stat is given
    if stat:
        return

    for market_code in market_code:
        pid = repository.get_ticker_pid(market_code)
        if pid:
            os.kill(pid, 9)

        cmd = f"PYTHONPATH=/usr/app/src/ python upbit/websocket.py --market-code {market_code}"
        pid = run_cmd(cmd)
        repository.update_ticker_pid(market_code, pid)


@router.post("/tickers/stop", response_model=None)
def turnoff_data(
    request_body: TickersList,
) -> None:
    """Stop websocket scraping for given market codes"""
    market_code = request_body.ticker_list

    check_market_code_valid(market_code)

    for market_code in market_code:
        pid = repository.get_ticker_pid(market_code)
        if pid:
            os.kill(pid, 9)
            repository.update_ticker_pid(market_code, None)
