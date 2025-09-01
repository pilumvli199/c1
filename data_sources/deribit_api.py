import requests
import pandas as pd

BASE_URL = "https://www.deribit.com/api/v2"

def get_instruments(currency="BTC", kind="option"):
    url = f"{BASE_URL}/public/get_instruments?currency={currency}&kind={kind}&expired=false"
    return requests.get(url).json()["result"]

def get_book_summary(instrument):
    url = f"{BASE_URL}/public/get_book_summary_by_instrument?instrument_name={instrument}"
    return requests.get(url).json()["result"][0]

def fetch_data(currency="BTC"):
    instruments = get_instruments(currency)
    chain_data = []
    for inst in instruments[:50]:
        summary = get_book_summary(inst["instrument_name"])
        chain_data.append({
            "instrument": inst["instrument_name"],
            "strike": inst.get("strike"),
            "expiry": inst["expiration_timestamp"],
            "option_type": inst.get("option_type"),
            "oi": summary["open_interest"],
            "iv": summary["iv"],
            "delta": summary.get("greeks", {}).get("delta"),
            "gamma": summary.get("greeks", {}).get("gamma"),
            "theta": summary.get("greeks", {}).get("theta"),
            "vega": summary.get("greeks", {}).get("vega"),
        })
    return pd.DataFrame(chain_data)
