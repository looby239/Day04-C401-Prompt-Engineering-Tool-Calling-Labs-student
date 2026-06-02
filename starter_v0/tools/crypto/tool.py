from __future__ import annotations
from typing import Any
import requests
from tools._shared import TIMEOUT, err

def get_crypto_price(symbol: str = "") -> dict[str, Any]:
    """
    Get the real-time price of a cryptocurrency from Binance public API.
    """
    if not symbol:
        return {"tool": "crypto", "error": "Missing symbol argument"}
    
    clean_sym = symbol.strip().upper()
    # Map common currency shorthand to USDT trading pair
    if clean_sym in ("BTC", "ETH", "BNB", "SOL", "ADA", "DOT", "XRP", "LTC", "DOGE"):
        query_sym = f"{clean_sym}USDT"
    elif not clean_sym.endswith("USDT") and not clean_sym.endswith("BTC") and not clean_sym.endswith("FDUSD"):
        query_sym = f"{clean_sym}USDT"
    else:
        query_sym = clean_sym
        
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        resp = requests.get(url, params={"symbol": query_sym}, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        return {
            "tool": "crypto",
            "symbol": clean_sym,
            "price": float(data.get("price", 0.0)),
            "pair": query_sym,
            "source": "Binance"
        }
    except Exception as exc:
        return err("crypto", exc)
