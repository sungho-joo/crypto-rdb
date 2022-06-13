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


def check_market_code_valid(market_codes: List[str]) -> None:
    """Check if market code is valid"""
    all_tickers = set(pyupbit.get_tickers())
    market_code_set = set(market_codes)

    if market_code_set - all_tickers != set():
        raise HTTPException(status_code=400, detail="Invalid market code")


def run_cmd(cmd: str) -> int:
    """Run command"""
    sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    return sp.pid
