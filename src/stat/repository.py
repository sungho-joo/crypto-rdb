# -*- coding: utf-8 -*-

"""
Data selection from tables related to crypto using SQLAlchemy ORM

Author:
    Name: Dongmin Lee
    Email: kid33629@gmail.com
"""

from contextlib import AbstractContextManager
from typing import Any, Callable, Dict, List, Tuple

import sqlalchemy as db
from sqlalchemy.orm import Session

from db.database import Database
from db.tables import Accum, Diff, Price, Ticker, Trade


class TickerDBRepository:
    """TickerDBRepository"""

    def __init__(
        self,
        session_factory: Callable[
            ...,
            AbstractContextManager[Session],  # pylint: disable=unsubscriptable-object
        ] = Database().session,
    ) -> None:
        self.session_factory = session_factory

    @classmethod
    def get_attributes(cls):
        """Get attributes of a class"""
        return [i for i in cls.__dict__ if i[:1] != "_"]

    def select_from_tables(self, stmt: db.sql.Select) -> Tuple[Dict[int, Tuple[Any, ...]], List[str]]:
        """Select data from tables"""
        rows = {}
        print(f"Statement: {stmt}")
        with self.session_factory() as session:
            results = session.execute(stmt)
            cols = list(results.keys())
            for i, record in enumerate(results):
                rows[i] = tuple(record)
        return rows, cols

    def get_all_market_codes(self) -> List[str]:
        """Get all market codes from ticker table"""
        stmt = db.select(Ticker.market_code)
        return [ticker[0] for ticker in self.select_from_tables(stmt)[0].values()]

    def get_all_market_ids(self) -> List[int]:
        """Get all market ids from ticker table"""
        stmt = db.select(Ticker.id)
        return [ticker_id[0] for ticker_id in self.select_from_tables(stmt)[0].values()]

    def get_some_market_codes(self, ids: List[int]) -> List[str]:
        """Get some market codes from ticker table"""
        stmt = db.select(Ticker.market_code, Ticker.market_code.in_(ids))
        return [ticker[0] for ticker in self.select_from_tables(stmt)[0].values()]

    def get_some_market_ids(self, codes: List[str]) -> List[int]:
        """Get some market ids from ticker table"""
        stmt = db.select(Ticker.id, Ticker.id.in_(codes))
        return [ticker_id[0] for ticker_id in self.select_from_tables(stmt)[0].values()]

    def get_all_data(self, ticker_id: int) -> Tuple[Dict[int, Tuple[Any, ...]], List[str]]:
        """Get all data about a ticker"""
        stmt = (
            db.select(
                Trade.trade_date,
                Trade.trade_time,
                Trade.trade_volume,
                Trade.trade_price,
                Accum.acc_ask_volume,
                Accum.acc_bid_volume,
                Accum.acc_trade_volume,
                Accum.acc_trade_price,
                Price.opening_price,
                Price.high_price,
                Price.low_price,
                Diff.closing_price,
                Diff.change_state,
                Diff.change_price,
                Diff.change_rate,
            )
            .join(Accum, Trade.id == Accum.id)
            .join(Price, Trade.id == Price.id)
            .join(Diff, Trade.id == Diff.id)
            .where(Trade.ticker_id == ticker_id)
        )
        rows, cols = self.select_from_tables(stmt)
        return rows, cols

    def get_trade_prices(self, ticker_id: int) -> Tuple[Dict[int, Tuple[Any, ...]], List[str]]:
        """Get trade prices about a ticker"""
        stmt = db.select(Trade.trade_price).where(Trade.ticker_id == ticker_id)
        rows, cols = self.select_from_tables(stmt)
        return rows, cols

    def get_acc_ask_volume(
        self,
        ticker_id: int,
        start_date: str,
        end_date: str,
    ) -> Tuple[Dict[int, Tuple[Any, ...]], List[str]]:
        """Get accumulated ask volume about a ticker"""
        stmt = (
            db.select(Trade.trade_date, Trade.trade_time, Accum.acc_ask_volume)
            .join(Accum, Trade.id == Accum.id)
            .where(
                db.and_(
                    Trade.ticker_id == ticker_id,
                    start_date <= Trade.trade_date,
                    Trade.trade_date <= end_date,
                )
            )
        )
        rows, cols = self.select_from_tables(stmt)
        return rows, cols

    def get_acc_bid_volume(
        self,
        ticker_id: int,
        start_date: str,
        end_date: str,
    ) -> Tuple[Dict[int, Tuple[Any, ...]], List[str]]:
        """Get accumulated bid volume about a ticker"""
        stmt = (
            db.select(Trade.trade_date, Trade.trade_time, Accum.acc_bid_volume)
            .join(Accum, Trade.id == Accum.id)
            .where(
                db.and_(
                    Trade.ticker_id == ticker_id,
                    start_date <= Trade.trade_date,
                    Trade.trade_date <= end_date,
                )
            )
        )
        rows, cols = self.select_from_tables(stmt)
        return rows, cols


if __name__ == "__main__":
    ticker_db_repository = TickerDBRepository()

    # Test 1: get_all_market_codes()
    codes = ticker_db_repository.get_all_market_codes()
    # print(codes)

    # Test 2: get_all_market_ids()
    ids = ticker_db_repository.get_all_market_ids()
    # print(ids)

    # Test 3: get_some_market_codes()
    market_codes = ["KRW-BTC", "KRW-ETH"]
    codes = ticker_db_repository.get_some_market_codes(market_codes)
    # print(codes)

    # Test 4: get_some_market_ids()
    market_ids = [1, 2]
    ids = ticker_db_repository.get_some_market_ids(market_ids)
    # print(ids)

    # Test 5: get_all_data()
    rows, cols = ticker_db_repository.get_all_data(1)
    # print(rows, cols)

    # Test 6: get_trade_prices()
    rows, cols = ticker_db_repository.get_trade_prices(1)
    # print(rows, cols)

    START_DATE = "2022-03-04"
    END_DATE = "2022-05-04"

    # Test 7: get_acc_ask_volume()
    rows, cols = ticker_db_repository.get_acc_ask_volume(1, START_DATE, END_DATE)
    # print(rows, cols)

    # Test 8: get_acc_bid_volume()
    rows, cols = ticker_db_repository.get_acc_bid_volume(1, START_DATE, END_DATE)
    # print(rows, cols)
