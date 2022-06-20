# -*- coding: utf-8 -*-
# mypy: ignore-errors

"""
API functions based on FastAPI

Author:
    Name: Sungho Joo
    Email: triangle124@gmail.com
"""

import os
import time
from typing import Optional

import pyupbit
from fastapi import APIRouter

from upbit.repository import UpbitDBRepository
from upbit.schema import TickerDataIn, TickerDataListOut, TickerDataOut, TickersList
from upbit.utils import check_market_code_valid, run_cmd

router = APIRouter(prefix="/upbit", tags=["upbit"], responses={404: {"description": "Not found"}})

repository = UpbitDBRepository()


@router.get("/tickers", response_model=TickersList)
def get_tickers() -> TickersList:
    """Get all tickers"""
    tickers = pyupbit.get_tickers()
    return TickersList(ticker_list=tickers)


@router.get("/tickers/active", response_model=TickerDataListOut)
def get_active_tickers() -> TickersList:
    """Get all active tickers"""
    ticker_pid = repository.get_active_tickers()
    return TickerDataListOut(
        ticker_list=[TickerDataOut(market_code=ticker, pid=pid) for ticker, pid in ticker_pid.items()],
    )


# pylint: disable=inconsistent-return-statements
@router.post("/tickers", response_model=TickerDataListOut)
def turnon_data(
    request_body: TickerDataIn,
) -> Optional[TickerDataListOut]:
    """Start websocket scraping for given market codes"""
    market_codes = request_body.market_codes
    stat = request_body.stat

    check_market_code_valid(market_codes)

    # TBD: when stat is given
    if stat:
        return

    ticker_data_list = []
    for market_code in market_codes:
        pid = repository.get_ticker_pid(market_code)
        if pid:
            os.kill(pid, 9)

        cmd = f"PYTHONPATH=/usr/app/src/ python upbit/websocket.py --market-code {market_code}"
        pid = run_cmd(cmd)

        cnt = 0
        while cnt < 30:
            if repository.check_ticker_existence(market_code):
                break
            cnt += 1
            time.sleep(1)

        repository.update_ticker_pid(market_code, pid)
        ticker_data_list.append(TickerDataOut(market_code=market_code, pid=pid))
    return TickerDataListOut(ticker_list=ticker_data_list)


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
