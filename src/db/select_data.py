# -*- coding: utf-8 -*-

"""
Data selection from tables related to crypto using SQLAlchemy ORM

Author:
    Name: Dongmin Lee
    Email: kid33629@gmail.com
"""

from typing import Any, List

import sqlalchemy as db
from sqlalchemy.orm import Session

from src.db.create_tables import Accum, Ticker, Trade, engine

# start_date = " "
# start_time = " "
# end_date = " "
# end_time = " "


def select_from_tables(stmt: db.sql.Select) -> List[Any]:
    """Select data from tables"""
    with Session(engine) as session:
        print(f"Columns: {list(session.execute(stmt).keys())}")
        records = session.execute(stmt).scalars().first()
        print(records)
        # for i, record in enumerate(records):
        #     print(f"{i}: {record}")
    return records


if __name__ == "__main__":
    stmt = db.select(Ticker.id)
    ticker_ids = select_from_tables(stmt)

    trade_prices = {}
    for ticker_id in ticker_ids:
        stmt = db.select(Trade.trade_price).where(Trade.ticker_id == ticker_id)
        trade_price = select_from_tables(stmt)
        trade_prices[ticker_id] = trade_price

    acc_bid_volumes = {}
    for ticker_id in ticker_ids:
        stmt = (
            db.select(Trade.trade_date, Trade.trade_time, Accum.acc_bid_volume)
            .join(Accum, Trade.id == Accum.id)
            .where(Trade.ticker_id == ticker_id)
        )
        acc_bid_volume = select_from_tables(stmt)
        acc_bid_volumes[ticker_id] = acc_bid_volume


# 2. 누적 거래량 (기간 설정 가능)
# select acc_bid_volume from accum where ticker_id = 1;
# select acc_bid_volume from accum where ticker_id = 2;
# select acc_bid_volume from accum where ticker_id = 3;

# select trade.trade_date, trade.trade_time, accum.acc_bid_volume
# from trade, accum where trade.id = accum.id and trade.ticker_id = 1 limit 5;

# 3. MA 10, 20, 50 - graph
