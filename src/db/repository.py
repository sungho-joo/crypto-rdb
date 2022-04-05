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

from src.db.database import Database
from src.db.tables import Accum, Diff, Price, Ticker, Trade

market_code = ["KRW-BTC", "KRW-ETH"]
START_DATE = "2022-03-04"
END_DATE = "2022-03-04"


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
        with self.session_factory as session:
            results = session.execute(stmt)
            cols = list(results.keys())
            for i, record in enumerate(results):
                rows[i] = tuple(record)
        return rows, cols

    def get_all_tickers(self) -> List[str]:
        """Get all tickers"""
        stmt = db.select(Ticker.market_code)
        return [ticker[0] for ticker in self.select_from_tables(stmt)[0].values()]

    def get_all_ticker_ids(self) -> List[int]:
        """Get all ticker ids"""
        stmt = db.select(Ticker.id)
        return [ticker_id[0] for ticker_id in self.select_from_tables(stmt)[0].values()]

    def get_all_data_about_ticker(self, ticker_id: int) -> Dict[str, Any]:
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


# if __name__ == "__main__":
#     stmt = db.select(Ticker.id)
#     ticker_ids: List[int] = [int(ticker_id[0]) for ticker_id in select_from_tables(stmt).values()]

#     trade_prices = {}
#     for ticker_id in ticker_ids:
#         stmt = db.select(Trade.trade_price).where(Trade.ticker_id == ticker_id)
#         trade_prices[ticker_id] = select_from_tables(stmt)

#     print(len(trade_prices[1]))
#     print(len(trade_prices[2]))

#     acc_bid_volumes = {}
#     for ticker_id in ticker_ids:
#         stmt = (
#             db.select(Trade.trade_date, Trade.trade_time, Accum.acc_bid_volume)
#             .join(Accum, Trade.id == Accum.id)
#             .where(
#                 db.and_(
#                     Trade.ticker_id == ticker_id,
#                     START_DATE <= Trade.trade_date,
#                     Trade.trade_date <= END_DATE,
#                 )
#             )
#         )
#         acc_bid_volumes[ticker_id] = select_from_tables(stmt)
