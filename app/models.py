from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__="products"

    id    = Column(Integer, primary_key=True, index=True)
    name  = Column(String, nullable=False)
    url   = Column(String, nullable=False)
    item_id = Column(String, unique=True, nullable=False)
    alert_price = Column(Float, nullable=True)

class PriceHistory(Base):
    __tablename__="price_history"

    id   = Column(Integer,primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price      = Column(Float, nullable=False)
    recorded_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )