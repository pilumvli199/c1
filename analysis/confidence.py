def calc_confidence(ta, oi, sentiment, pattern):
    """
    Combine TA, OI, sentiment, and candlestick pattern signals
    into a single confidence score (0–100).
    """
    score = 0

    if ta:        # technical indicators
        score += 25
    if oi:        # options open interest
        score += 25
    if sentiment: # sentiment analysis
        score += 25
    if pattern:   # candlestick pattern
        score += 25

    return score


def calculate_levels(price, direction="LONG", target_pct=0.2, sl_pct=0.1):
    """
    Calculate target and stoploss levels based on entry price and direction.
    """
    if direction.upper() == "LONG":
        target = round(price * (1 + target_pct), 2)
        sl = round(price * (1 - sl_pct), 2)
    else:  # SHORT
        target = round(price * (1 - target_pct), 2)
        sl = round(price * (1 + sl_pct), 2)
    return target, sl


def generate_signal(symbol, price, confidence, direction="LONG"):
    """
    Generate formatted signal message with entry, target, stoploss.
    """
    target, sl = calculate_levels(price, direction)
    signal_msg = f"""
⚡ {symbol} {direction.upper()} Options Signal
Confidence: {confidence}%
Entry: {price}
🎯 Target: {target}
🛑 StopLoss: {sl}
"""
    return signal_msg


