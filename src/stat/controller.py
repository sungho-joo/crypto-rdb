# -*- coding: utf-8 -*-
# mypy: ignore-errors

"""
API functions based on FastAPI

Author:
    Name: Sungho Joo
    Email: triangle124@gmail.com
"""

from stat.repository import TickerDBRepository
from stat.schema import StatGetOut, StatsGetOut, TickersGetOut
from typing import Any, Dict, List, Optional, Tuple

from fastapi import APIRouter, Query

repository = TickerDBRepository()

router = APIRouter(prefix="/stat", tags=["stat"], responses={404: {"description": "Not found"}})


@router.get("/tickers", response_model=TickersGetOut)
def get_tickers() -> TickersGetOut:
    """Get all tickers"""
    tickers = repository.get_all_market_codes()
    return TickersGetOut(ticker_list=tickers)


@router.get("/")
def get_all_stat_data_for_given_tickers(
    query_params: Optional[List[str]] = Query(None, description="List of market code"),
) -> StatsGetOut:
    """Get all data for given tickers"""
    if not query_params:
        ticker_ids = repository.get_all_market_ids()
    else:
        ticker_ids = repository.get_some_market_ids(query_params)
    ans = []
    for ticker_id in ticker_ids:
        all_stat_data: Tuple[Dict[int, Tuple[Any, ...]], List[str]] = repository.get_all_data(ticker_id)
        ans.append(all_stat_data)
    return ans


@router.get("/price/", response_model=StatsGetOut)
def get_current_price(
    query_params: Optional[List[str]] = Query(None, description="List of market code"),
) -> StatsGetOut:
    """Get price for given market code"""
    if not query_params:
        ticker_ids = repository.get_all_market_ids()
    else:
        ticker_ids = repository.get_some_market_ids(query_params)
    price_list = []
    for ticker_id in ticker_ids:
        price, cols = repository.get_trade_prices(ticker_id)
        price_list.append(StatGetOut(stat_name=cols[0], value=price))
    return StatsGetOut(stats=price_list)


@router.get("/ask/accumulation/{start_date}-{end_date}")
def get_ask_accumlation_range(
    start_date: str,
    end_date: str,
    query_params: Optional[List[str]] = Query(None, description="List of market code"),
) -> StatsGetOut:
    """Get ask accumulation for given time period for given market code"""

    if not query_params:
        ticker_ids = repository.get_all_market_ids()
    else:
        ticker_ids = repository.get_some_market_ids(query_params)

    ans = []
    for ticker_id in ticker_ids:
        price, cols = repository.get_acc_ask_volume(ticker_id, start_date, end_date)
        ans.extend([price, cols])
    return ans


@router.get("/bid/accumulation/{start_date}-{end_date}")
def get_bid_accumlation_range(
    start_date: str,
    end_date: str,
    query_params: Optional[List[str]] = Query(None, description="List of market code"),
) -> StatsGetOut:
    """Get bid accumulation for given time period for given market code"""

    if not query_params:
        ticker_ids = repository.get_all_market_ids()
    else:
        ticker_ids = repository.get_some_market_ids(query_params)

    ans = []
    for ticker_id in ticker_ids:
        price, cols = repository.get_acc_bid_volume(ticker_id, start_date, end_date)
        ans.extend([price, cols])
    return ans
