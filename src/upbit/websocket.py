# -*- coding: utf-8 -*-
# mypy: ignore-errors

"""
Data insertion into tables related to crypto using SQLAlchemy ORM

Author:
    Name: Dongmin Lee
    Email: kid33629@gmail.com
"""

import argparse
from contextlib import AbstractAsyncContextManager
from typing import Callable, Dict, List

import sqlalchemy as sa
from pyupbit import WebSocketManager
from sqlalchemy.orm import Session

from db.database import Database
from db.model import Accum, Diff, Price, Ticker, Trade

Database().create_database()


class UpbitWebSocket:
    """Websocket wrapper Class"""

    def __init__(
        self,
        ext_websocket: WebSocketManager,
        market_code: List[str] = ["KRW-BTC"],
        session_factory: Callable[
            ...,
            AbstractAsyncContextManager[Session],  # pylint: disable=unsubscriptable-object
        ] = Database().session,
    ):
        self.market_code = market_code
        self.session_factory = session_factory
        self._websocket = ext_websocket

    def get_existing_tickers(self, stmt: sa.sql.Select) -> List[Ticker]:
        """Get existing records from Ticker table"""
        with self.session_factory() as session:
            records = session.execute(stmt).all()
        return records

    def insert_into_ticker_table(self, market_code: str) -> None:
        """Insert data into Ticker table"""
        selected_code = set()
        for record in self.get_existing_tickers(sa.select(Ticker)):
            selected_code.add(record[0].market_code)

        objects = []
        if market_code not in selected_code:
            objects.append(
                Ticker(id=None, market_code=market_code),
            )

        with self.session_factory() as session:
            session.add_all(objects)
            session.commit()

    def insert_into_other_tables(self, code_idx: Dict[str, int]) -> None:
        """Insert data into other tables (e.g., Trade, Accum, Price, Diff)"""
        while True:
            data = self._websocket.get()

            objects = [
                Trade(
                    id=None,
                    trade_date=data["trade_date"],
                    trade_time=data["trade_time"],
                    trade_volume=data["trade_volume"],
                    trade_price=data["trade_price"],
                    ticker_id=code_idx[data["code"]],
                ),
                Accum(
                    id=None,
                    acc_ask_volume=data["acc_ask_volume"],
                    acc_bid_volume=data["acc_bid_volume"],
                    acc_trade_volume=data["acc_trade_volume"],
                    acc_trade_price=data["acc_trade_price"],
                    ticker_id=code_idx[data["code"]],
                ),
                Price(
                    id=None,
                    opening_price=data["opening_price"],
                    high_price=data["high_price"],
                    low_price=data["low_price"],
                    ticker_id=code_idx[data["code"]],
                ),
                Diff(
                    id=None,
                    closing_price=data["prev_closing_price"],
                    change_state=data["change"],
                    change_price=data["change_price"],
                    change_rate=data["change_rate"],
                    ticker_id=code_idx[data["code"]],
                ),
            ]

            with self.session_factory() as session:
                session.add_all(objects)
                session.commit()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--market-code", type=str, nargs="+", help="market code")
    args = argparser.parse_args()

    websocket = UpbitWebSocket(
        ext_websocket=WebSocketManager("ticker", args.market_code),
        market_code=args.market_code,
    )

    websocket.insert_into_ticker_table(args.market_code)

    websocket.insert_into_other_tables(args.market_code)
