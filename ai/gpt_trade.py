import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gpt_trade_decision(coin, data, oi, sentiment, pattern):
    short_input = (
        f"COIN:{coin} | PCR:{oi['pcr']} | SUP:{oi['support']} | RES:{oi['resistance']}\n"
        f"PATTERN:{pattern}\n"
        f"NEWS:{sentiment['news']} | TOKEN:{sentiment['token']} | MACRO:{sentiment['macro']}"
    )
    prompt = (
        "Task: Give trading signal in SHORT format.\n"
        "Output only in this format:\n"
        "DIR: LONG/SHORT/NO TRADE\n"
        "ENTRY: xxxx\n"
        "SL: xxxx\n"
        "TARGET: xxxx\n"
        "CONF: xx%\n"
        f"\nDATA:\n{short_input}"
    )
    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
        max_output_tokens=80
    )
    return response.output_text.strip()
