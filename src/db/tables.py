# -*- coding: utf-8 -*-

"""
Creation for tables related to crypto using SQLAlchemy ORM

Author:
    Name: Dongmin Lee
    Email: kid33629@gmail.com
"""

import sqlalchemy as db

from db.database import Base


class Ticker(Base):  # pylint: disable=too-few-public-methods
    """
    Ticker table class
    """

    __tablename__ = "ticker"

    id = db.Column(db.Integer, primary_key=True)
    market_code = db.Column(db.VARCHAR(20), nullable=False)

    def __repr__(self) -> str:
        return f"Ticker(id={self.id!r}, market_code={self.market_code!r})"


class Trade(Base):  # pylint: disable=too-few-public-methods
    """
    Trade table class
    """

    __tablename__ = "trade"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trade_date = db.Column(db.DATE, nullable=False)
    trade_time = db.Column(db.TIME, nullable=False)
    trade_volume = db.Column(db.FLOAT(30), nullable=False)
    trade_price = db.Column(db.FLOAT(30), nullable=False)
    ticker_id = db.Column(
        db.Integer,
        db.ForeignKey("ticker.id", ondelete="RESTRICT", onupdate="CASCADE"),
    )

    def __repr__(self) -> str:
        return (
            f"Trade(id={self.id!r}, trade_date={self.trade_date!r}, "
            f"trade_time={self.trade_time!r}, trade_volume={self.trade_volume!r}, "
            f"trade_price={self.trade_price!r}, ticker_id={self.ticker_id!r})"
        )


class Accum(Base):  # pylint: disable=too-few-public-methods
    """
    Accumulation table class
    """

    __tablename__ = "accum"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    acc_ask_volume = db.Column(db.FLOAT(30), nullable=False)
    acc_bid_volume = db.Column(db.FLOAT(30), nullable=False)
    acc_trade_volume = db.Column(db.FLOAT(30), nullable=False)
    acc_trade_price = db.Column(db.FLOAT(30), nullable=False)
    ticker_id = db.Column(
        db.Integer,
        db.ForeignKey("ticker.id", ondelete="RESTRICT", onupdate="CASCADE"),
    )

    def __repr__(self) -> str:
        return (
            f"Accum(id={self.id!r}, acc_ask_volume={self.acc_ask_volume!r}, "
            f"acc_bid_volume={self.acc_bid_volume!r}, acc_trade_volume={self.acc_trade_volume!r}, "
            f"acc_trade_price={self.acc_trade_price!r}, ticker_id={self.ticker_id!r})"
        )


class Price(Base):  # pylint: disable=too-few-public-methods
    """
    Price table class
    """

    __tablename__ = "price"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    opening_price = db.Column(db.FLOAT(30), nullable=False)
    high_price = db.Column(db.FLOAT(30), nullable=False)
    low_price = db.Column(db.FLOAT(30), nullable=False)
    ticker_id = db.Column(
        db.Integer,
        db.ForeignKey("ticker.id", ondelete="RESTRICT", onupdate="CASCADE"),
    )

    def __repr__(self) -> str:
        return (
            f"Price(id={self.id!r}, opening_price={self.opening_price!r},"
            f"high_price={self.high_price!r}, low_price={self.low_price!r}, "
            f"ticker_id={self.ticker_id!r})"
        )


class Diff(Base):  # pylint: disable=too-few-public-methods
    """
    Difference table class
    """

    __tablename__ = "diff"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    closing_price = db.Column(db.FLOAT(30), nullable=False)
    change_state = db.Column(db.VARCHAR(10), nullable=False)
    change_price = db.Column(db.FLOAT(30), nullable=False)
    change_rate = db.Column(db.FLOAT(30), nullable=False)
    ticker_id = db.Column(
        db.Integer,
        db.ForeignKey("ticker.id", ondelete="RESTRICT", onupdate="CASCADE"),
    )

    def __repr__(self) -> str:
        return (
            f"Diff(id={self.id!r}, closing_price={self.closing_price!r}, "
            f"change_state={self.change_state!r}, change_price={self.change_price!r}, "
            f"change_rate={self.change_rate!r}, ticker_id={self.ticker_id!r})"
        )
