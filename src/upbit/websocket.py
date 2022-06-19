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

argparser = argparse.ArgumentParser()
argparser.add_argument("--market-code", type=str, nargs="+", help="market code")


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

    def get_existing_tickers(self, stmt: sa.sql.Select) -> Dict[str, int]:
        """Get existing records from Ticker table"""
        with self.session_factory() as session:
            records = session.execute(stmt).all()

        existed_code = dict()
        for idx, record in enumerate(records):
            existed_code[record[0].market_code] = idx
        return existed_code

    def insert_into_ticker_table(self, market_code: str) -> None:
        """Insert data into Ticker table"""
        existed_code = self.get_existing_tickers(sa.select(Ticker))

        objects = []
        if market_code not in existed_code:
            objects.append(
                Ticker(id=None, market_code=market_code),
            )

        with self.session_factory() as session:
            session.add_all(objects)
            session.commit()

    def insert_into_other_tables(self, market_code: str) -> None:
        """Insert data into other tables (e.g., Trade, Accum, Price, Diff)"""
        existed_code = self.get_existing_tickers(sa.select(Ticker))

        while True:
            data = self._websocket.get()
            assert (
                market_code == data["code"]
            ), "The market code is different a code from the websocket."

            objects = [
                Trade(
                    id=None,
                    trade_date=data["trade_date"],
                    trade_time=data["trade_time"],
                    trade_volume=data["trade_volume"],
                    trade_price=data["trade_price"],
                    ticker_id=existed_code[market_code],
                ),
                Accum(
                    id=None,
                    acc_ask_volume=data["acc_ask_volume"],
                    acc_bid_volume=data["acc_bid_volume"],
                    acc_trade_volume=data["acc_trade_volume"],
                    acc_trade_price=data["acc_trade_price"],
                    ticker_id=existed_code[market_code],
                ),
                Price(
                    id=None,
                    opening_price=data["opening_price"],
                    high_price=data["high_price"],
                    low_price=data["low_price"],
                    ticker_id=existed_code[market_code],
                ),
                Diff(
                    id=None,
                    closing_price=data["prev_closing_price"],
                    change_state=data["change"],
                    change_price=data["change_price"],
                    change_rate=data["change_rate"],
                    ticker_id=existed_code[market_code],
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
