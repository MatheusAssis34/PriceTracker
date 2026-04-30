from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, create_tables
from app.models import Product, PriceHistory
from app.scraper import search_product, get_current_price
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Price Tracker", version = "1.0.0")

create_tables()

class ProductCreate(BaseModel):
    item_id: str
    name:    str
    url:     str
    alert_price: Optional[float] = None

class ProductResponse(BaseModel):
    id:      int
    item_id: str
    name:    str
    url:     str
    alert_price: Optional[float]

    class Config:
        from_attributes = True