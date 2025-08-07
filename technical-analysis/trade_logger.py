import json
import os

TRADES_FILE = "trades.json"

def log_trade(symbol, entry_price, targets, stop_loss, analysis_type, rating):
    trade = {
        "symbol": symbol,
        "entry_price": entry_price,
        "targets": targets,
        "stop_loss": stop_loss,
        "analysis_type": analysis_type,
        "rating": rating,
        "status": "open"
    }

    if not os.path.exists(TRADES_FILE):
        with open(TRADES_FILE, 'w') as f:
            json.dump([], f)

    with open(TRADES_FILE, 'r') as f:
        trades = json.load(f)

    trades.append(trade)

    with open(TRADES_FILE, 'w') as f:
        json.dump(trades, f, indent=4)

def update_trade_result(symbol, current_price):
    if not os.path.exists(TRADES_FILE):
        return

    with open(TRADES_FILE, 'r') as f:
        trades = json.load(f)

    updated = []
    for trade in trades:
        if trade["symbol"] == symbol and trade["status"] == "open":
            if current_price >= max(trade["targets"]):
                trade["status"] = "target_hit"
            elif current_price <= trade["stop_loss"]:
                trade["status"] = "stopped_out"
        updated.append(trade)

    with open(TRADES_FILE, 'w') as f:
        json.dump(updated, f, indent=4)
