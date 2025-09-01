import os
import telebot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

bot = None
if TELEGRAM_BOT_TOKEN and ":" in TELEGRAM_BOT_TOKEN:
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
else:
    print("⚠️ Invalid TELEGRAM_BOT_TOKEN: Please set a valid token with a colon.")


def send_message(message: str):
    """Send generic startup/info messages"""
    if bot:
        try:
            if TELEGRAM_CHAT_ID:
                bot.send_message(TELEGRAM_CHAT_ID, message)
            else:
                print("⚠️ TELEGRAM_CHAT_ID not set.")
        except Exception as e:
            print(f"⚠️ Failed to send message: {e}")
    else:
        print(message)


def send_alert(message: str):
    """Send trading signal alerts"""
    if bot:
        try:
            if TELEGRAM_CHAT_ID:
                bot.send_message(TELEGRAM_CHAT_ID, message)
            else:
                print("⚠️ TELEGRAM_CHAT_ID not set.")
        except Exception as e:
            print(f"⚠️ Failed to send alert: {e}")
    else:
        print(message)
