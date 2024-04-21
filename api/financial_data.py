import json
from eodhd import APIClient
import pandas as pd


class EODHDAPIsDataFetcher:
    def __init__(self, api_token):
        self._api_token = api_token

    def fetch_exchanges(self):
        try:
            print("Fetching exchanges data from EoD backend")
            api = APIClient(self._api_token)
            df = api.get_exchanges()
            return json.loads(df.to_json(orient="records"))

        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def fetch_exchange_markets(self, code: str = ""):
        try:
            print("Fetching market data from EoD backend")
            api = APIClient(self._api_token)
            df = api.get_exchange_symbols(code)
            return json.loads(df.to_json(orient="records"))

        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def fetch_exchange_market_data(self, code: str = "", market: str = "", granularity: str = ""):
        try:
            print("Fetching stock data from EoD backend")
            api = APIClient(self._api_token)
            # df = api.get_ # api.get_historical_data(f"{market}.{code}", granularity)
            data = {
                'datetime': ['2024-04-01', '2024-04-02', '2024-04-03'],
                'open': [100.0, 102.5, 101.2],
                'high': [105.0, 103.8, 102.7],
                'low': [98.5, 100.2, 99.0],
                'close': [103.2, 101.0, 100.5],
                'volume': [10000, 12000, 9500]
            }
            df = pd.DataFrame(data)
            # df["datetime"] = df.index.astype(str)
            print(df)
            return json.loads(df.to_json(orient="records"))

        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
