import time
from config import COINS, SCAN_INTERVAL
from alerts.telegram_bot import send_message, send_alert
from data_sources.deribit_api import fetch_data, fetch_candles
from analysis.technicals import calc_indicators
from analysis.options_oi import analyze_oi
from analysis.candlesticks import summarize_candles
from analysis.sentiment import get_sentiment
from analysis.confidence import calc_confidence, generate_signal
from ai.gpt_trade import gpt_trade_decision


if __name__ == "__main__":
    send_message("🤖 Bot Started ✅ Now scanning every 30 minutes...")
    while True:
        for coin in COINS:
            try:
                # fetch index price
                data = fetch_data(coin)
                if not data:
                    print(f"⚠️ Skipping {coin}: no index price")
                    continue
                price = data["price"]

                # fetch candle data
                candles = fetch_candles(coin, resolution="5")  # 5-minute candles
                if not candles:
                    print(f"⚠️ Skipping {coin}: no candles")
                    continue

                # analysis
                ta = calc_indicators(candles)
                oi = analyze_oi(coin)
                pattern = summarize_candles(candles)
                sentiment = get_sentiment(coin)

                # confidence calculation
                confidence = calc_confidence(ta, oi, sentiment, pattern)

                if confidence >= 65:
                    # AI trade decision
                    gpt_signal = gpt_trade_decision(coin, candles, oi, sentiment, pattern)

                    # Decide direction
                    direction = "LONG" if "BUY" in gpt_signal.upper() else "SHORT"

                    # Generate formatted signal
                    msg = generate_signal(coin, price, confidence, direction)

                    # Send to Telegram
                    send_alert(msg)
                else:
                    print(f"[{coin}] Low confidence ({confidence}%) → No trade")

            except Exception as e:
                print(f"❌ Error with {coin}: {e}")

        time.sleep(SCAN_INTERVAL)
