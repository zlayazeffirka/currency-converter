from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RequestLog(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    base_currency = Column(String(3), nullable=False)
    target_currency = Column(String(3), nullable=False)
    amount = Column(Numeric(18, 6), nullable=False)
    result = Column(Numeric(18, 6), nullable=False)
    rate = Column(Numeric(18, 10), nullable=False)
    requested_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        {"postgresql_using": "btree"},
    )