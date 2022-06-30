# -*- coding: utf-8 -*-
# mypy: ignore-errors

"""
SDK for request data from DB

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
        url: str = "http://localhost:7777",
        ticker_list: List[str] = ["KRW-BTC"],
    ) -> None:
        self._url = url + "/stats/"
        self.ticker_list = ticker_list
        self._stats = ["price", "bid_accumulation", "ask_accumulation"]

    @property
    def stats(self) -> List[str]:
        """Get stats"""
        return self._stats

    def __repr__(self):
        return f"Data getter for {self.ticker_list}"

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
        url = self._url + self._get_stat_name(stat_name) + "/"
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
            "market_code": self.ticker_list,
            "start_date": start_date,
            "end_date": end_date,
        }
