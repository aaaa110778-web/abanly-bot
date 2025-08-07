import json
import os
from datetime import datetime

# المسار الافتراضي لتخزين سجل الصفقات
LOG_FILE = "trade_logger/trade_log.json"

def log_trade(symbol, strategy, entry_price, targets=None, stop_loss=None, score=None):
    trade = {
        "symbol": symbol.upper(),
        "strategy": strategy,
        "entry_price": entry_price,
        "targets": targets if targets else [],
        "stop_loss": stop_loss,
        "score": score,
        "entry_time": datetime.now().isoformat(),
        "status": "open",
        "result": None
    }

    trades = load_trades()
    trades.append(trade)
    save_trades(trades)

def update_trade_result(symbol, result_type, final_price):
    trades = load_trades()
    for trade in trades:
        if trade["symbol"].upper() == symbol.upper() and trade["status"] == "open":
            trade["status"] = "closed"
            trade["exit_time"] = datetime.now().isoformat()
            trade["exit_price"] = final_price
            trade["result"] = result_type  # "target_hit", "stop_loss_hit", "manual"
            adjust_strategy_learning(trade)
            break
    save_trades(trades)

def load_trades():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as file:
        return json.load(file)

def save_trades(trades):
    with open(LOG_FILE, "w") as file:
        json.dump(trades, file, indent=2)

def adjust_strategy_learning(trade):
    # نموذج بسيط لتحسين نسبة التقييم أو تعديل قرار البوت بناءً على نتائج الصفقات السابقة
    print(f"[LEARNING] Adjusting strategy for {trade['symbol']} based on result: {trade['result']}")
    # مثال: يمكن تعديل طريقة التقييم لاحقًا هنا باستخدام البيانات المتراكمة
