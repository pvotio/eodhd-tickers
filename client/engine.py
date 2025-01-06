from client.eodhd import EODHD
from config import logger, settings


class Engine:

    TOKEN = settings.TOKEN

    def __init__(self):
        self.exchanges = []
        self.tickers = []
        self.eodhd = EODHD(self.TOKEN)

    def run(self):
        logger.info(f"Fetching exchanges list")
        self.exchanges = self.eodhd.get_exchanges()
        logger.info(f"Fetched {len(self.exchanges)} exchanges")
        logger.info(f"Fetching tickers list")
        self._fetch_tickers()

    def _fetch_tickers(self):
        for exch in self.exchanges:
            exch_code = exch["Code"]
            logger.debug(f"Fetching {exch_code} exchange tickers")
            self._fetch_exchange_tickers(exch_code)

    def _fetch_exchange_tickers(self, exch_code):
        exch_tickers = self.eodhd.get_tickers(exch_code)
        for ticker_dict in exch_tickers:
            if not "Code" in ticker_dict:
                continue

            self.tickers.append(self._construct_ticker(ticker_dict, exch_code))

    def _construct_ticker(self, ticker_dict, exch_code):
        new_ticker_dict = {
            "ext2_ticker": f"{ticker_dict["Code"]}.{exch_code}",
            "CodeExchange": exch_code,
            **ticker_dict,
        }
        return new_ticker_dict
