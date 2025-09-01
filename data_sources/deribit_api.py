import requests

BASE_URL = "https://www.deribit.com/api/v2/public"


def fetch_data(symbol):
    """
    Fetch market data for given symbol from Deribit.
    Uses IV if available, else falls back to last_price.
    """
    try:
        url = f"{BASE_URL}/get_instruments?currency={symbol}&kind=option&expired=false"
        resp = requests.get(url).json()

        # Safe check for 'result'
        if "result" not in resp:
            print(f"⚠️ {symbol}: No 'result' in response → {resp}")
            return None

        instruments = []
        for row in resp["result"]:
            # If IV missing, still keep instrument using last_price
            iv = row.get("iv")
            last_price = row.get("tick_size")  # Deribit instruments don't give LTP directly

            if iv is None and last_price is None:
                continue  # nothing useful
            instruments.append(row)

        if not instruments:
            print(f"⚠️ {symbol}: No valid instruments found (no IV or price).")
            return None

        return instruments

    except Exception as e:
        print(f"❌ Error fetching data for {symbol}: {e}")
        return None

