# -*- coding: utf-8 -*-
# mypy: ignore-errors

"""
API functions based on FastAPI

Author:
    Name: Sungho Joo
    Email: triangle124@gmail.com
"""

from fastapi import APIRouter

from stats.repository import TickerDBRepository
from stats.schema import StatGetIn, StatGetOut, StatsGetOut, TickersGetOut
from stats.utils import check_date_valid

repository = TickerDBRepository()

router = APIRouter(prefix="/stat", tags=["stat"], responses={404: {"description": "Not found"}})


@router.get("/tickers", response_model=TickersGetOut)
def get_tickers() -> TickersGetOut:
    """Get all tickers"""
    tickers = repository.get_all_market_codes()
    return TickersGetOut(ticker_list=tickers)


@router.post("/price/", response_model=StatsGetOut)
def get_price_ranges(
    request_body: StatGetIn,
) -> StatsGetOut:
    """Get price for given market code"""
    market_code = request_body.market_code
    start_date = request_body.start_date
    end_date = request_body.end_date

    if not market_code:
        ticker_ids = repository.get_all_market_ids()
    else:
        ticker_ids = repository.get_some_market_ids(market_code)

    check_date_valid(start_date, end_date)

    price_list = []
    for i, ticker_id in enumerate(ticker_ids):
        price, cols = repository.get_price_ranges(ticker_id, start_date, end_date)
        price_list.append(StatGetOut(stat_name=cols[0], value=price, market_code=market_code[i]))
    return StatsGetOut(stats=price_list)


@router.post("/ask/accumulation/", response_model=StatsGetOut)
def get_ask_accumlation_range(
    request_body: StatGetIn,
) -> StatsGetOut:
    """Get ask accumulation for given time period for given market code"""
    market_code = request_body.market_code
    start_date = request_body.start_date
    end_date = request_body.end_date

    if not market_code:
        ticker_ids = repository.get_all_market_ids()
    else:
        ticker_ids = repository.get_some_market_ids(market_code)

    check_date_valid(start_date, end_date)

    ask_accum_list = []
    for i, ticker_id in enumerate(ticker_ids):
        ask_acc, cols = repository.get_acc_ask_volume(ticker_id, start_date, end_date)
        ask_accum_list.append(StatGetOut(stat_name=cols[0], value=ask_acc, market_code=market_code[i]))
    return StatsGetOut(stats=ask_accum_list)


@router.post("/bid/accumulation/", response_model=StatsGetOut)
def get_bid_accumlation_range(
    request_body: StatGetIn,
) -> StatsGetOut:
    """Get bid accumulation for given time period for given market code"""
    market_code = request_body.market_code
    start_date = request_body.start_date
    end_date = request_body.end_date

    if not market_code:
        ticker_ids = repository.get_all_market_ids()
    else:
        ticker_ids = repository.get_some_market_ids(market_code)

    check_date_valid(start_date, end_date)

    bid_accum_list = []
    for i, ticker_id in enumerate(ticker_ids):
        bid_accum, cols = repository.get_acc_bid_volume(ticker_id, start_date, end_date)
        bid_accum_list.append(
            StatGetOut(stat_name=cols[0], value=bid_accum, market_code=market_code[i]),
        )
    return StatsGetOut(stats=bid_accum_list)
