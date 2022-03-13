# -*- coding: utf-8 -*-

"""
Data selection from tables related to crypto using SQLAlchemy ORM

Author:
    Name: Dongmin Lee
    Email: kid33629@gmail.com
"""

from typing import Any, Dict, List, Tuple

import sqlalchemy as db
from sqlalchemy.orm import Session

from src.db.create_tables import Accum, Ticker, Trade, engine

START_DATE = "2022-03-04"
START_TIME = "12:33:07"
END_DATE = "2022-03-04"
END_TIME = "12:37:39"


def select_from_tables(stmt: db.sql.Select) -> Dict[int, Tuple[Any, ...]]:
    """Select data from tables"""
    record_dict = {}
    with Session(engine) as session:
        print(f"Statement: {stmt}")
        for i, record in enumerate(session.execute(stmt)):
            record_dict[i] = tuple(record)
    return record_dict


if __name__ == "__main__":
    stmt = db.select(Ticker.id)
    ticker_ids: List[int] = [int(ticker_id) for ticker_id in select_from_tables(stmt)]

    trade_prices = {}
    for ticker_id in ticker_ids:
        stmt = db.select(Trade.trade_price).where(Trade.ticker_id == ticker_id)
        trade_prices[ticker_id] = select_from_tables(stmt)

    acc_bid_volumes = {}
    for ticker_id in ticker_ids:
        stmt = (
            db.select(Trade.trade_date, Trade.trade_time, Accum.acc_bid_volume)
            .join(Accum, Trade.id == Accum.id)
            .where(
                db.and_(
                    Trade.ticker_id == ticker_id,
                    START_DATE <= Trade.trade_date,
                    START_TIME <= Trade.trade_time,
                    Trade.trade_date <= END_DATE,
                    Trade.trade_time <= END_TIME,
                )
            )
        )
        acc_bid_volumes[ticker_id] = select_from_tables(stmt)
