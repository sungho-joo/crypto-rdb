from fastapi import APIRouter
from repository import StatRepository
from typing import List, Dict, Any

repository = StatRepository()

router = APIRouter(
    prefix="/stat",
    tags=["stat"],
    responses={404: {"description": "Not found"}}
)

@router.get("/tickers")
def get_tickers():
    tickers = repository.get_tickers()
    return tickers

@router.get("/tickers")
def get_all_stat_data_for_given_tickers(query_params: List[str]):
    ticker_ids = repository.get_ticker_ids(query_params)
    ans = []
    for ticker_id in ticker_ids:
        all_stat_data: Dict[str, Any] = repository.get_all_data_about_ticker(ticker_id)
        ans.append(all_stat_data)
    
    return ans

