import httpx
from datetime import date
from typing import Optional

EXCHANGE_API_BASE = "https://api.frankfurter.app"

async def fetch_rate(base: str, target: str, dt: Optional[date] = None) -> float:
    if dt is None:
        dt = date.today()
    elif dt > date.today():
        raise ValueError("Future dates are not supported")

    endpoint = "latest" if dt == date.today() else dt.isoformat()
    url = f"{EXCHANGE_API_BASE}/{endpoint}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            url,
            params={
                "base": base.upper().strip(),
            }
        )
        resp.raise_for_status()
        data = resp.json()

        rates = data.get("rates", {})
        if target.upper() not in rates:
            raise ValueError(f"Target currency '{target.upper()}' not available for base '{base.upper()}'")

        return float(rates[target.upper()])