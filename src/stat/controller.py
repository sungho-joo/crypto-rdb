# -*- coding: utf-8 -*-

"""
TBU

Author:
    Name:
    Email:
"""

from typing import Any, Dict

from fastapi import APIRouter

from src.stat.repository import TickerDBRepository

repository = TickerDBRepository()

router = APIRouter(prefix="/stat", tags=["stat"], responses={404: {"description": "Not found"}})


@router.get("/tickers")
def get_tickers():
    """Get all tickers"""
    tickers = repository.get_all_tickers()
    return tickers


@router.get("/tickers")
def get_all_stat_data_for_given_tickers():
    """Get all data for given tickers"""
    ticker_ids = repository.get_all_ticker_ids()
    ans = []
    for ticker_id in ticker_ids:
        all_stat_data: Dict[str, Any] = repository.get_all_data_about_ticker(ticker_id)
        ans.append(all_stat_data)
    return ans
