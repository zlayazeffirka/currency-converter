from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ConversionRequest(BaseModel):
    base: str
    target: str
    amount: float
    date: Optional[str] = None  

class ConversionResponse(BaseModel):
    result: float
    rate: float
    requested_at: datetime

class RequestLogOut(BaseModel):
    id: int
    base_currency: str
    target_currency: str
    amount: float
    result: float
    rate: float
    requested_at: datetime

    class Config:
        from_attributes = True