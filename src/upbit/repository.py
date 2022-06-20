# -*- coding: utf-8 -*-

"""
Repository related to upbit using SQLAlchemy ORM

Author:
    Name: Sungho Joo
    Email: triangle124@gmail.com
"""

from contextlib import AbstractContextManager
from typing import Any, Callable, Dict

import sqlalchemy as sa
from sqlalchemy.orm import Session

from db.database import Database
from db.model import Ticker


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

    def check_ticker_existence(self, market_code: str) -> bool:
        """Check ticker existence from ticker table"""

        stmt = sa.select(Ticker.market_code).where(Ticker.market_code == market_code)
        with self.session_factory() as session:
            ticker_code = session.execute(stmt).fetchone()
        return bool(ticker_code is not None)

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

        return pid[0] if pid else None

    def get_active_tickers(self) -> Dict[str, Any]:
        """Get active tickers from ticker table"""

        stmt = sa.select(Ticker.market_code, Ticker.pid).where(Ticker.pid.is_not(None))

        with self.session_factory() as session:
            ticker_pid_list = session.execute(stmt).fetchall()
            return dict(tuple(ticker_pid_list))
