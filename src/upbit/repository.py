# -*- coding: utf-8 -*-

"""
Repository related to upbit using SQLAlchemy ORM

Author:
    Name: Sungho Joo
    Email: triangle124@gmail.com
"""

from contextlib import AbstractContextManager
from typing import Any, Callable, List

import sqlalchemy as sa
from sqlalchemy.orm import Session

from db.database import Database
from db.tables import Ticker


class UpbitDBRepository:
    """UpbitDBRepository"""

    def __init__(
        self,
        session_factory: Callable[
            ...,
            AbstractContextManager[Session],  # pylint: disable=unsubscriptable-object
        ] = Database().session,
    ) -> None:
        self.session_factory = session_factory

    def update_ticker_pid(self, market_code: str, pid: int) -> None:
        """Insert pid to pid table"""

        stmt = sa.update(Ticker).where(Ticker.market_code == market_code).values(pid=pid)
        with self.session_factory() as session:
            session.execute(stmt)
            session.commit()

    def remove_ticker_pid(self, market_code: str) -> None:
        """Remove pid from pid table"""

        stmt = sa.update(Ticker).where(Ticker.market_code == market_code).values(pid=None)
        with self.session_factory() as session:
            session.execute(stmt)
            session.commit()

    def get_ticker_pid(self, market_code: str) -> Any:
        """Get pid from pid table"""

        stmt = sa.select(Ticker.pid).where(Ticker.market_code == market_code)
        with self.session_factory() as session:
            pid = session.execute(stmt).fetchone()

        print(market_code, pid)
        return pid[0] if pid else None

    def get_active_tickers(self) -> List[str]:
        """Get active tickers from ticker table"""

        stmt = sa.select(Ticker.market_code).where(Ticker.pid is not None)

        with self.session_factory() as session:
            tickers = session.execute(stmt).fetchall()
        return [ticker[0] for ticker in tickers]
