import requests

BASE_URL = "https://www.deribit.com/api/v2/public"


def fetch_data(symbol):
    """
    Fetch market data for given symbol from Deribit.
    Handles missing keys safely.
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
            iv = row.get("iv")
            if iv is None:
                # Skip if no IV
                continue
            instruments.append(row)

        if not instruments:
            print(f"⚠️ {symbol}: No valid instruments with IV found.")
            return None

        return instruments

    except Exception as e:
        print(f"❌ Error fetching data for {symbol}: {e}")
        return None
