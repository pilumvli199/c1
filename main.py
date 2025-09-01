import time
from config import COINS, SCAN_INTERVAL
from alerts.telegram_bot import send_message, send_alert
from data_sources.deribit_api import fetch_data
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
                # fetch data safely
                data = fetch_data(coin)
                if not data:
                    print(f"⚠️ Skipping {coin}: no data")
                    continue

                # analysis
                ta = calc_indicators(data)
                oi = analyze_oi(coin)
                pattern = summarize_candles(data)
                sentiment = get_sentiment(coin)

                # confidence calculation
                confidence = calc_confidence(ta, oi, sentiment, pattern)

                if confidence >= 65:
                    # AI trade decision
                    gpt_signal = gpt_trade_decision(coin, data, oi, sentiment, pattern)

                    # Safely extract price
                    price = None
                    if isinstance(data, dict) and "close" in data:
                        price = data["close"][-1]
                    elif isinstance(data, list) and "last_price" in data[0]:
                        price = data[0]["last_price"]
                    else:
                        print(f"⚠️ No close price found for {coin}, skipping")
                        continue

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
