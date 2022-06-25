# -*- coding: utf-8 -*-

"""
API functions based on FastAPI

Author:
    Name: Sungho Joo
    Email: triangle124@gmail.com
"""

import subprocess
from typing import List

import pyupbit
from fastapi import HTTPException


def check_ticker_valid(ticker_list: List[str]) -> None:
    """Check if ticker is valid"""
    all_tickers = set(pyupbit.get_tickers())
    ticker_set = set(ticker_list)

    if ticker_set - all_tickers != set():
        raise HTTPException(status_code=400, detail="Invalid ticker")


def run_cmd(cmd: str) -> int:
    """Run command"""
    sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    return sp.pid
