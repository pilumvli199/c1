import requests

BASE_URL = "https://www.deribit.com/api/v2/public"


def fetch_data(symbol):
    """
    Fetch market data for given symbol from Deribit.
    Returns index price for proper Entry/Target/SL calculation.
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
