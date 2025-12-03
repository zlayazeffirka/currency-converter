import os
from datetime import date
from typing import List, Optional

from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker, Session
from prometheus_fastapi_instrumentator import Instrumentator

from models import Base, RequestLog
from schemas import ConversionRequest, ConversionResponse, RequestLogOut
from services.exchange import fetch_rate
from services.prediction import get_last_n_rates, simple_trend_prediction

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@db:5432/currency")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Курсовик — Конвертер валют",
    description="USD → RUB и не только",
    version="1.0"
)

Instrumentator().instrument(app).expose(app, include_in_schema=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/convert")
async def convert(
    base: str = Query(..., min_length=3), 
    target: str = Query(..., min_length=3), 
    amount: float = Query(..., gt=0), 
    date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        dt = date.fromisoformat(date) if date else None
        rate = await fetch_rate(base.upper(), target.upper(), dt)
        result = round(amount * rate, 6)

        log = RequestLog(
            base_currency=base.upper(),
            target_currency=target.upper(),
            amount=amount,
            result=result,
            rate=rate
        )
        db.add(log)
        db.commit()

        return {"result": result, "rate": rate}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}
@app.get("/history", response_model=List[RequestLogOut])
def get_history(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    stmt = select(RequestLog).order_by(RequestLog.requested_at.desc()).limit(limit).offset(offset)
    return db.scalars(stmt).all()

@app.get("/predict")
async def predict_rate(base: str, target: str, db: Session = Depends(get_db)):
    rate = await fetch_rate(base.upper(), target.upper())
    return {
        "result": rate,
        "rate": rate,
        "requested_at": datetime.utcnow() + timedelta(days=1)
    }