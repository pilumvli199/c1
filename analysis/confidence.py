def calculate_levels(price, direction="LONG", target_pct=0.2, sl_pct=0.1):
    if direction.upper() == "LONG":
        target = round(price * (1 + target_pct), 2)
        sl = round(price * (1 - sl_pct), 2)
    else:  # SHORT
        target = round(price * (1 - target_pct), 2)
        sl = round(price * (1 + sl_pct), 2)
    return target, sl

def generate_signal(symbol, price, confidence, direction="LONG"):
    target, sl = calculate_levels(price, direction)
    signal_msg = f"""
⚡ {symbol} {direction.upper()} Options Signal
Confidence: {confidence}%
Entry: {price}
🎯 Target: {target}
🛑 StopLoss: {sl}
"""
    return signal_msg

