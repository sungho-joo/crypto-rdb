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
from upbit.utils import check_ticker_valid, run_cmd

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
        ticker_list=[TickerDataOut(ticker=ticker, pid=pid) for ticker, pid in ticker_pid.items()],
    )


# pylint: disable=inconsistent-return-statements
@router.post("/tickers/subscribe", response_model=TickerDataListOut)
def subscibe_data(
    request_body: TickerDataIn,
) -> Optional[TickerDataListOut]:
    """Start websocket scraping for given ticker list"""
    ticker_list = request_body.ticker_list
    stat = request_body.stats

    check_ticker_valid(ticker_list)

    # TBD: when stat is given
    if stat:
        return

    ticker_data_list = []
    for ticker in ticker_list:
        pid = repository.get_ticker_pid(ticker)
        if pid:
            os.kill(pid, 9)

        cmd = f"PYTHONPATH=/usr/app/src/ python upbit/websocket.py --market-code {ticker}"
        pid = run_cmd(cmd)

        cnt = 0
        while cnt < 30:
            if repository.check_ticker_existence(ticker):
                break
            cnt += 1
            time.sleep(1)

        repository.update_ticker_pid(ticker, pid)
        ticker_data_list.append(TickerDataOut(ticker=ticker, pid=pid))
    return TickerDataListOut(ticker_list=ticker_data_list)


@router.post("/tickers/unsubscribe", response_model=TickerDataListOut)
def unsubscribe_data(
    request_body: TickersList,
) -> TickerDataListOut:
    """Stop websocket scraping for given ticker list"""
    ticker_list = request_body.ticker_list

    check_ticker_valid(ticker_list)

    ticker_data_list = []
    for ticker in ticker_list:
        pid = repository.get_ticker_pid(ticker)
        if pid:
            os.kill(pid, 9)
            repository.update_ticker_pid(ticker, None)
        ticker_data_list.append(TickerDataOut(ticker=ticker, pid=pid))
    return TickerDataListOut(ticker_list=ticker_data_list)
