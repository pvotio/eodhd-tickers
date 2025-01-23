from client.eodhd import EODHD
from config import logger, settings


class Engine:

    TOKEN = settings.TOKEN

    def __init__(self, exchanges):
        self.exchanges = exchanges
        self.tickers = []
        self.eodhd = EODHD(self.TOKEN)

    def run(self):
        logger.info("Fetching tickers for each exchange...")
        self._fetch_tickers()
        logger.info(
            f"Completed fetching tickers. Total tickers accumulated: {len(self.tickers)}"
        )

    def _fetch_tickers(self):
        for exch in self.exchanges:
            logger.debug(f"Fetching {exch} exchange tickers")
            self._fetch_exchange_tickers(exch)

    def _fetch_exchange_tickers(self, exch_code):
        exch_tickers = self.eodhd.get_tickers(exch_code)
        logger.debug(f"Fetched {len(exch_tickers)} tickers for exchange: {exch_code}")
        for ticker_dict in exch_tickers:
            if not "Code" in ticker_dict:
                continue

            self.tickers.append(self._construct_ticker(ticker_dict, exch_code))

    def _construct_ticker(self, ticker_dict, exch_code):
        new_ticker_dict = {
            "eodhd_ticker": f"{ticker_dict['Code']}.{exch_code}",
            "CodeExchange": exch_code,
            **ticker_dict,
        }
        return new_ticker_dict
