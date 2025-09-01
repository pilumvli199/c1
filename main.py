import time
from config import COINS, SCAN_INTERVAL
from alerts.telegram_bot import send_message, send_signal
from data_sources.deribit_api import fetch_data
from analysis.technicals import calc_indicators
from analysis.options_oi import analyze_oi
from analysis.candlesticks import summarize_candles
from analysis.sentiment import get_sentiment
from analysis.confidence import calc_confidence
from ai.gpt_trade import gpt_trade_decision

if __name__ == "__main__":
    send_message("🤖 Bot Started ✅ Now scanning every 30 minutes...")
    while True:
        for coin in COINS:
            try:
                data = fetch_data(coin)
                ta = calc_indicators(data)
                oi = analyze_oi(coin)
                pattern = summarize_candles(data)
                sentiment = get_sentiment(coin)
                confidence = calc_confidence(ta, oi, sentiment, pattern)
                if confidence >= 65:
                    gpt_signal = gpt_trade_decision(coin, data, oi, sentiment, pattern)
                    send_signal(coin, gpt_signal, confidence)
                else:
                    print(f"[{coin}] Low confidence ({confidence}%) → No trade")
            except Exception as e:
                print(f"Error with {coin}: {e}")
        time.sleep(SCAN_INTERVAL)
