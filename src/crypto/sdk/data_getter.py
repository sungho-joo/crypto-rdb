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
        self._stats = ["price", "bid_accumulation", "ask_accumulation"]

    @property
    def stats(self) -> List[str]:
        """Get stats"""
        return self._stats

    @classmethod
    def _get_stat_name(cls, stat_name: str) -> str:
        stat_dict = {
            "price": "price",
            "bid_accumulation": "bid/accumulation",
            "ask_accumulation": "ask/accumulation",
        }
        return stat_dict[stat_name]

    def get_stat_data(self, stat_name: str, start_date: str, end_date: str) -> str:
        """Get stat"""
        headers = {"Content-Type": "application/json"}
        url = self._url + "/stat/" + self._get_stat_name(stat_name) + "/"
        payload = self._get_payload(start_date, end_date)

        response = requests.post(url, headers=headers, json=payload)
        status_code, response_body = (
            response.status_code,
            response.json(),
        )

        if status_code == 200:
            return response_body
        else:
            return f"Error occured while getting data: {response_body}"

    def _get_payload(self, start_date: str, end_date: str) -> Dict[str, Any]:
        return {
            "market_code": self.market_codes,
            "start_date": start_date,
            "end_date": end_date,
        }
