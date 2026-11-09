"""Percentage-based demonstration logic extracted from NCAP app/planner.py.
Source blob: ade68b5a9c626e402fa3f8670c4b7a654cd533ac.
Placeholder calculations only; not a production risk model.
"""
def basic_exit_prices(direction: str, signal_price: float):
    if direction == "LONG":
        stop = signal_price * (1 - 0.003)
        tp1 = signal_price * (1 + 0.006)
        tp2 = signal_price * (1 + 0.010)
    else:
        stop = signal_price * (1 + 0.003)
        tp1 = signal_price * (1 - 0.006)
        tp2 = signal_price * (1 - 0.010)
    return stop, tp1, tp2

