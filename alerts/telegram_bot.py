import telebot
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def send_message(msg: str):
    bot.send_message(CHAT_ID, msg)

def send_signal(coin, gpt_signal, confidence):
    msg = (f"⚡ {coin} Options Signal\n\n"
           f"{gpt_signal}\n"
           f"Confidence: {confidence}%")
    bot.send_message(CHAT_ID, msg)
