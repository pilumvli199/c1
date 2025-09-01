import requests

BASE_URL = "https://www.deribit.com/api/v2/public"


def fetch_data(symbol):
    """
    Fetch index price for given coin (BTC, ETH, SOL, XRP).
    This is used for Entry, Target, StopLoss calculation.
    """
    try:
        url = f"{BASE_URL}/get_index_price?index_name={symbol.lower()}_usd"
        resp = requests.get(url).json()

        if "result" not in resp:
            print(f"⚠️ {symbol}: No 'result' in response → {resp}")
            return None

        index_price = resp["result"].get("index_price")
        if not index_price:
            print(f"⚠️ {symbol}: No index price found → {resp}")
            return None

        return {"price": index_price}

    except Exception as e:
        print(f"❌ Error fetching data for {symbol}: {e}")
        return None


def fetch_candles(symbol, resolution="5"):
    """
    Fetch OHLCV candles for given coin using Deribit perpetual futures.
    resolution = "1" (1 min), "5" (5 min), "15" (15 min), "60" (1H), "1D" etc.
    """
    try:
        instrument = f"{symbol}-PERPETUAL"
        url = (
            f"{BASE_URL}/get_tradingview_chart_data"
            f"?instrument_name={instrument}&resolution={resolution}"
            f"&start_timestamp=1725148800000&end_timestamp=1725235200000"
        )

        resp = requests.get(url).json()

        if "result" not in resp:
            print(f"⚠️ {symbol}: No candle data → {resp}")
            return None

        return resp["result"]

    except Exception as e:
        print(f"❌ Error fetching candles for {symbol}: {e}")
        return None
