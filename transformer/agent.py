from datetime import datetime

import pandas as pd

from config import settings


class Agent:

    def __init__(self, exchanges, tickers):
        self.exchanges = exchanges
        self.tickers = tickers
        self.tables = {}
        self.dataframes = {}

    def transform(self):
        self._transform_exchanges()
        self._transform_tickers()
        self._init_dataframes()
        return self.dataframes

    def _transform_exchanges(self):
        self.tables[settings.EXCHANGES_OUTPUT_TABLE] = []
        for exchange in self.exchanges:
            self.tables[settings.EXCHANGES_OUTPUT_TABLE].append(
                {**exchange, "timestamp_created_utc": self.timenow()}
            )

    def _transform_tickers(self):
        self.tables[settings.TICKERS_OUTPUT_TABLE] = []
        for ticker in self.tickers:
            if ".FOREX" in ticker["eodhd_ticker"]:
                pair = ticker["eodhd_ticker"]
                if len(pair) == 6:
                    ticker["Currency"] = pair[3:]
                else:
                    ticker["Currency"] = pair

            self.tables[settings.TICKERS_OUTPUT_TABLE].append(
                {
                    **{k: self._convert_to_none(v) for k, v in ticker.items()},
                    "timestamp_created_utc": self.timenow(),
                }
            )

    def _init_dataframes(self):
        for t, data in self.tables.items():
            self.dataframes[t] = pd.DataFrame(data)

    @staticmethod
    def _convert_to_none(value):
        if value in ["NA", "NaN", "", 0, "0", None]:
            return None

        return value

    @staticmethod
    def timenow():
        return datetime.utcnow()
