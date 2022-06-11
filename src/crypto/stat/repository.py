# -*- coding: utf-8 -*-

"""
Data selection from tables related to crypto using SQLAlchemy ORM

Author:
    Name: Dongmin Lee
    Email: kid33629@gmail.com
"""

import datetime
from contextlib import AbstractContextManager
from typing import Any, Callable, Dict, List, Tuple

import sqlalchemy as db
from sqlalchemy.orm import Session

from crypto.db.database import Database
from crypto.db.tables import Accum, Diff, Price, Ticker, Trade


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
        return [ticker_name[0] for ticker_name in self.select_from_tables(stmt)[0].values()]

    def get_all_market_ids(self) -> List[int]:
        """Get all market ids from ticker table"""
        stmt = db.select(Ticker.id)
        return [ticker_id[0] for ticker_id in self.select_from_tables(stmt)[0].values()]

    def get_some_market_codes(self, ids: List[str]) -> List[str]:
        """Get some market codes from ticker table"""
        stmt = db.select(Ticker.market_code, Ticker.market_code.in_(ids))
        return [ticker[0] for ticker in self.select_from_tables(stmt)[0].values()]

    def get_some_market_ids(self, codes: List[int]) -> List[int]:
        """Get some market ids from ticker table"""
        stmt = db.select(Ticker.id).where(Ticker.market_code.in_(codes))
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

    def get_price_ranges(
        self,
        ticker_id: int,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> Tuple[Dict[int, Tuple[Any, ...]], List[str]]:
        """Get trade prices about a ticker"""
        stmt = db.select(Trade.trade_date, Trade.trade_time, Trade.trade_price).where(
            db.and_(
                Trade.ticker_id == ticker_id,
                start_date <= Trade.trade_date,
                Trade.trade_date <= end_date,
            ),
        )
        rows, cols = self.select_from_tables(stmt)
        return rows, cols

    def get_acc_ask_volume(
        self,
        ticker_id: int,
        start_date: datetime.date,
        end_date: datetime.date,
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
                ),
            )
        )
        rows, cols = self.select_from_tables(stmt)
        return rows, cols

    def get_acc_bid_volume(
        self,
        ticker_id: int,
        start_date: datetime.date,
        end_date: datetime.date,
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
                ),
            )
        )
        rows, cols = self.select_from_tables(stmt)
        return rows, cols
