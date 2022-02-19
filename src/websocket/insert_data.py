# -*- coding: utf-8 -*-

"""
Data insertion into tables related to crypto using SQLAlchemy ORM

Author:
    Name: Dongmin Lee
    Email: kid33629@gmail.com
"""

from typing import Dict, List

import pyupbit
import sqlalchemy as db
from sqlalchemy.orm import Session

from src.db.create_tables import Accum, Diff, Price, Ticker, Trade, engine

market_code = ["KRW-BTC", "KRW-ETH"]


def get_existing_tickers(stmt: db.sql.Select) -> List[Ticker]:
    """Get existing records from Ticker table"""
    with Session(engine) as session:
        print(f"Columns: {list(session.execute(stmt).keys())}")
        records = session.execute(stmt).scalars().all()
        for i, record in enumerate(records):
            print(f"{i}: {record}")
    return records


def insert_into_ticker_table(code_idx: Dict[str, int]) -> None:
    """Insert data into Ticker table"""
    records = get_existing_tickers(db.select(Ticker))

    selected_code = set()
    for record in records:
        selected_code.add(record.market_code)

    objects = []
    for key, value in code_idx.items():
        if key not in selected_code:
            objects.append(
                Ticker(id=value, market_code=key),
            )

    with Session(engine) as session:
        session.add_all(objects)
        session.commit()


def insert_into_other_tables(web_socket: pyupbit.WebSocketManager, code_idx: Dict[str, int]) -> None:
    """Insert data into other tables (e.g., Trade, Accum, Price, Diff)"""
    while True:
        data = web_socket.get()

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

        with Session(engine) as session:
            session.add_all(objects)
            session.commit()


if __name__ == "__main__":
    all_tickers = pyupbit.get_tickers()
    assert all(code in all_tickers for code in market_code), "Not exist market_code list in all_tickers"

    market_code_idx = {}
    for i, code in enumerate(market_code):
        market_code_idx[code] = i + 1
    insert_into_ticker_table(market_code_idx)

    web_socket = pyupbit.WebSocketManager("ticker", market_code)
    insert_into_other_tables(web_socket, market_code_idx)
