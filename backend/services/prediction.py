import httpx
from datetime import date, timedelta
from typing import List, Optional

async def get_last_n_rates(base: str, target: str, n: int = 7) -> List[float]:
    rates = []
    today = date.today()
    for i in range(n):
        dt = today - timedelta(days=i)
        try:
            rate = await fetch_rate_simple(base, target, dt)
            if rate is not None:
                rates.append(rate)
            if len(rates) >= n:
                break
        except Exception:
            continue
    return rates[:n]

async def fetch_rate_simple(base: str, target: str, dt: date) -> Optional[float]:
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(
            f"https://api.frankfurter.app/{dt.isoformat()}",
            params={
                "from": base.strip().upper(),   
                "to": target.strip().upper()    
            }
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        return data["rates"].get(target.upper())
    
def simple_trend_prediction(rates: List[float]) -> float:
    if not rates:
        raise ValueError("No historical rates available")
    n = len(rates)
    avg = sum(rates) / n
    if n < 2:
        return avg
    trend = (rates[0] - rates[-1]) / (n - 1) if n > 1 else 0
    prediction = avg + 0.5 * trend
    return max(prediction, 0.0001)