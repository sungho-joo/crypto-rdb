# -*- coding: utf-8 -*-
# mypy: ignore-errors

"""
API functions based on FastAPI

Author:
    Name: Sungho Joo
    Email: triangle124@gmail.com
"""

from typing import Any, Dict, List

import pandas as pd
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

    def __repr__(self):
        return f"Data getter for {self.market_codes}"

    @classmethod
    def _get_stat_name(cls, stat_name: str) -> str:
        stat_dict = {
            "price": "price",
            "bid_accumulation": "bid/accumulation",
            "ask_accumulation": "ask/accumulation",
        }
        return stat_dict[stat_name]

    def get_stat_range_data(self, stat_name: str, start_date: str, end_date: str) -> str:
        """Get stat"""
        headers = {"Content-Type": "application/json"}
        url = self._url + "/stats/" + self._get_stat_name(stat_name) + "/"
        payload = self._get_payload(start_date, end_date)

        response = requests.post(url, headers=headers, json=payload)

        status_code, response_body = response.status_code, response.json()

        if status_code == 200:
            ret = dict()
            for data in response_body["stats"]:
                ret[data["market_code"]] = pd.DataFrame.from_dict(
                    data["value"],
                    orient="index",
                    columns=["Trade date", "Trade time", data["stat_name"]],
                )
            return ret
        else:
            raise Exception(f'Error occured while getting data: {response_body["detail"]}')

    def _get_payload(self, start_date: str, end_date: str) -> Dict[str, Any]:
        return {
            "market_code": self.market_codes,
            "start_date": start_date,
            "end_date": end_date,
        }
