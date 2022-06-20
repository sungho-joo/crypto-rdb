# -*- coding: utf-8 -*-

"""
API functions based on FastAPI

Author:
    Name: Sungho Joo
    Email: triangle124@gmail.com
"""

from datetime import date

from fastapi import HTTPException


def _check_date_format(date_str: str) -> bool:
    """Check if date is in ISO format"""
    try:
        date.fromisoformat(date_str)
        return True
    except ValueError:
        return False


def check_date_valid(start_date: str, end_date: str) -> None:
    """Check if date is valid"""
    if not _check_date_format(start_date) or not _check_date_format(end_date):
        raise HTTPException(status_code=400, detail="Date is not in ISO format")

    if start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date must be before end_date")
