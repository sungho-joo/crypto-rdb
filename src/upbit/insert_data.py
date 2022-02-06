# -*- coding: utf-8 -*-

"""
Data insertion related to crypto using SQLAlchemy ORM from tables

Author:
    Name: Dongmin Lee
    Email: kid33629@gmail.com
"""

from typing import List

import pyupbit
import sqlalchemy as db
from sqlalchemy.orm import Session

from src.db.create_tables import Accumulation, Change, Price, Ticker, Trade, engine

market_code = ["KRW-BTC", "KRW-ETH"]


def select(stmt: db.sql) -> List[Ticker]:
    """Select function"""
    rows = []
    with Session(engine) as session:
        print(list(session.execute(stmt).keys()))
        for row in session.execute(stmt):
            rows.append(row)
            print(row)
        print("\n")
    return rows


if __name__ == "__main__":
    all_tickers = pyupbit.get_tickers()

    market_code_idx = {}
    for i, code in enumerate(market_code):
        market_code_idx[code] = i + 1

    wm = pyupbit.WebSocketManager("ticker", market_code)

# if ticker에 데이터가 존재하면, pass
# otherwise 실행
# select count(*) from ticker
results = select(db.select(Ticker))
for elem in results:
    print(f"id : {elem[0].id}, market_code: {elem[0].market_code}")
print(results)

objects = []
for code in market_code:
    objects.append(
        Ticker(id=None, market_code=code),
    )

with Session(engine) as session:
    session.add_all(objects)
    session.commit()

select(db.select(Ticker))


while True:
    data = wm.get()

    objects = [
        Trade(
            id=None,
            trade_date=data["trade_date"],
            trade_time=data["trade_time"],
            trade_volume=data["trade_volume"],
            ticker_id=market_code_idx[data["code"]],
        ),
        Accumulation(
            id=None,
            acc_ask_volume=data["acc_ask_volume"],
            acc_bid_volume=data["acc_bid_volume"],
            acc_trade_volume=data["acc_trade_volume"],
            acc_trade_price=data["acc_trade_price"],
            ticker_id=market_code_idx[data["code"]],
        ),
        Price(
            id=None,
            opening_price=data["opening_price"],
            high_price=data["high_price"],
            low_price=data["low_price"],
            trade_price=data["trade_price"],
            ticker_id=market_code_idx[data["code"]],
        ),
        Change(
            id=None,
            closing_price=data["prev_closing_price"],
            change_state=data["change"],
            change_price=data["change_price"],
            change_rate=data["change_rate"],
            ticker_id=market_code_idx[data["code"]],
        ),
    ]

    with Session(engine) as session:
        session.add_all(objects)
        session.commit()

    # select(db.select(Trade))
    # select(db.select(Accumulation))
    # select(db.select(Price))
    # select(db.select(Change))

wm.terminate()
