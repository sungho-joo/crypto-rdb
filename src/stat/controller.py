# -*- coding: utf-8 -*-

"""
TBU

Author:
    Name:
    Email:
"""

from typing import Any, Dict, Tuple, List, Optional

from fastapi import APIRouter, Query

from .repository import TickerDBRepository

repository = TickerDBRepository()

router = APIRouter(prefix="/stat", tags=["stat"], responses={404: {"description": "Not found"}})


@router.get("/tickers")
def get_tickers():
    """Get all tickers"""
    tickers = repository.get_all_tickers()
    return tickers


@router.get("/")
def get_all_stat_data_for_given_tickers():
    """Get all data for given tickers"""
    ticker_ids = repository.get_all_ticker_ids()
    ans = []
    for ticker_id in ticker_ids:
        all_stat_data: Tuple[Dict[int, Tuple[Any, ...]], List[str]] = repository.get_all_data(ticker_id)
        ans.append(all_stat_data)
    return ans

@router.get("/price/")
def get_current_price(query_param: Optional[List[str]] = None):
    if not query_param:
        ticker_ids = repository.get_all_ticker_ids()
    else:
        ticker_ids = repository.get_ticker_ids(query_param)
    ans = []
    for ticker_id in ticker_idx:
        price, _ = repository.get_trade_prices(ticker_id)
        ans.append(price)
    return ans


@rouger.get("/ask/accumulation/{start_date}-{end_date}")
def get_ask_accumlation_range(start_date: str, end_date: str, query_param: Optional[List[str]] = None):
    if not query_param:
        ticker_ids = repository.get_all_ticker_ids()
    else:
        ticker_ids = repository.get_ticker_ids(query_param)

    ans = []
    for ticker_id in ticker_ids:
        price, _ = repository.get_acc_ask_volume(ticker_id, start_date, end_date)
        ans.append(price)
    return ans


@rouger.get("/bid/accumulation/{start_date}-{end_date}")
def get_bid_accumlation_range(start_date: str, end_date: str, query_param: Optional[List[str]] = None):
    if not query_param:
        ticker_ids = repository.get_all_ticker_ids()
    else:
        ticker_ids = repository.get_ticker_ids(query_param)

    ans = []
    for ticker_id in ticker_ids:
        price, _ = repository.get_acc_bid_volume(ticker_id, start_date, end_date)
        ans.append(price)
    return ans

