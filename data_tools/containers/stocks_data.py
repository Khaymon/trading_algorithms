from .time_data_container import TimeDataContainer

import os
import pandas as pd
import numpy as np
from typing import List, Tuple, Any, Union


class StocksData(TimeDataContainer):
    def __init__(self, files: Union[List[str], str] = None, data: pd.DataFrame = None):
        if data is not None:
            self.data = data
        else:
            if isinstance(files, List):
                dfs_list = []
                for file in files:
                    dfs_list.append(StocksData.read_ticker_data(file))
            
                self.data = pd.concat(dfs_list)
            else:
                self.data = StocksData.read_ticker_data(files)
        self.tickers = self.data["ticker"].unique()
        
    
    def _construct(self, data: pd.DataFrame):
        return StocksData(data=data)
        
    
    def get_columns(self, key: Any = None):
        data = self.data.copy()
        if key is None:
            return self._construct(data=data)
        else:
            return self._construct(data=data[key])


    def get_tickers(self) -> List[str]:
        return self.tickers


    def add_feature(self, feature: pd.DataFrame):
        self.data = self.data.merge(feature, how="left", on=["date", "ticker"])


    def filter_ticker(self, ticker: str):
        return StocksData(data=self.data[self.data["ticker"] == ticker].copy())

        
    @staticmethod
    def read_ticker_data(file_path: str) -> pd.DataFrame:
        data = pd.read_csv(file_path, parse_dates=["date"])
        
        data = data.set_index("date")
        data = data.sort_index()
        data = data.dropna()
        
        return data