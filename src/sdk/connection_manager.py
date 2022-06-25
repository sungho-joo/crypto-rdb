# -*- coding: utf-8 -*-
# mypy: ignore-errors

"""
SDK for managing websocket connection to Upbit

Author:
    Name: Sungho Joo
    Email: triangle124@gmail.com
"""

from typing import List, Optional

import pandas as pd
import requests


class ConnManager:
    """Connection manager for websocket connection to Upbit"""

    def __init__(
        self,
        url: str = "http://localhost:7777",
    ):
        self._available_ticker_list = pd.DataFrame()
        self._active_tickers = pd.DataFrame(columns=["ticker"])
        self._url = url + "/upbit"
        self._ticker_pid_map = dict()

    @property
    def available_ticker_list(self):
        """Get available ticker list"""
        if len(self._available_ticker_list):
            return self._available_ticker_list

        headers = {"Content-Type": "application/json"}
        url = self._url + "/tickers"

        response = requests.get(url, headers=headers)

        status_code, response_body = response.status_code, response.json()
        if status_code == 200:
            self._available_ticker_list = pd.DataFrame(
                data=response_body["ticker_list"],
                columns=["ticker"],
            )
            return self._available_ticker_list
        else:
            raise Exception(f'Error occured while getting data: {response_body["detail"]}')

    @property
    def active_tickers(self):
        """Get active tickers"""
        headers = {"Content-Type": "application/json"}
        url = self._url + "/tickers/active"

        response = requests.get(url, headers=headers)
        status_code, response_body = response.status_code, response.json()
        if status_code == 200:
            self._active_tickers = pd.DataFrame(
                data=[ticker_data["ticker"] for ticker_data in response_body["ticker_list"]],
                columns=["ticker"],
            )
            return self._active_tickers
        else:
            raise Exception(f'Error occured while getting data: {response_body["detail"]}')

    def subscibe_tickers(self, ticker_list: List[str], stats: Optional[str] = None):
        """Subscribe to tickers of interest"""
        headers = {"Content-Type": "application/json"}
        url = self._url + "/tickers/subscribe"
        payload = {
            "ticker_list": ticker_list,
            "stats": stats,
        }

        response = requests.post(url, headers=headers, json=payload)
        status_code, response_body = response.status_code, response.json()
        if status_code == 200:
            subscribed = []
            for data in response_body["ticker_list"]:
                self._ticker_pid_map[data["ticker"]] = data["pid"]
                subscribed.append(data["ticker"])
            print(f"Subscribed tickers: {subscribed}")
        else:
            raise Exception(f'Error occured while subscribing data: {response_body["detail"]}')

    def unsubscribe_tickers(self, ticker_list: List[str]):
        """Unsubscribe to tickers of interest"""
        headers = {"Content-Type": "application/json"}
        url = self._url + "/tickers/unsubscribe"
        payload = {
            "ticker_list": ticker_list,
        }

        response = requests.post(url, headers=headers, json=payload)
        status_code, response_body = response.status_code, response.json()
        if status_code == 200:
            unsubscribed = []
            for data in response_body["ticker_list"]:
                self._ticker_pid_map.pop(data["ticker"])
                unsubscribed.append(data["ticker"])
            print(f"Unsubscribed tickers: {unsubscribed}")
        else:
            raise Exception(f'Error occured while unsubscribing data: {response_body["detail"]}')
