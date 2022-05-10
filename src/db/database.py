# -*- coding: utf-8 -*-

"""
Creation for tables related to crypto using SQLAlchemy ORM

Author:
    Name: Dongmin Lee
    Email: kid33629@gmail.com
"""

from contextlib import AbstractContextManager, contextmanager
from typing import Callable

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

config = {
    "host": "db",
    "user": "root",
    "port": 3306,
    "password": 20220201,
    "database": "crypto-rdb",
}

db_host = config.get("host")
db_user = config.get("user")
db_port = config.get("port")
db_pwd = config.get("password")
db_name = config.get("database")

CONNECTION_URL = f"mariadb+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}"
Base = declarative_base()


class Database:
    """Database"""

    def __init__(self, db_url: str = CONNECTION_URL) -> None:
        self._engine = create_engine(db_url)
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        """
        create all tables
        """
        Base.metadata.create_all(bind=self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        """
        create database session with contextmanager to
        do some CRUD thing
        """
        session: Session = self._session_factory()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
