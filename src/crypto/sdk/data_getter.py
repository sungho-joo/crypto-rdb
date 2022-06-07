# -*- coding: utf-8 -*-
# mypy: ignore-errors

"""
API functions based on FastAPI

Author:
    Name: Sungho Joo
    Email: triangle124@gmail.com
"""

from typing import Any, Dict, List

import requests


class DataGetter:
    """DataGetter"""

    def __init__(
        self,
        url: str = "http://localhost:8888",
        market_codes: List[str] = ["KRW-BTC"],
    ) -> None:
        self._url = url
        self.market_codes = market_codes

    def get_price_data(self, start_date: str, end_date: str) -> str:
        """Get data"""
        headers = {"Content-Type": "application/json"}
        url = self._url + "/stat/price/"
        payload = self._get_payload(start_date, end_date)
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def _get_payload(self, start_date: str, end_date: str) -> Dict[str, Any]:
        return {
            "market_code": self.market_codes,
            "start_date": start_date,
            "end_date": end_date,
        }
