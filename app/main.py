from app.scheduler import scheduler, check_all_prices
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, create_tables
from app.models import Product, PriceHistory
from app.scraper import search_product, get_current_price
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Price Tracker", version = "1.0.0")

@app.on_event("startup")
def start_scheduler():
    scheduler.start()
    print("scheduler iniciado. Verificação de preços a cada 1 hora.")

@app.on_event("shutdown")
def stop_scheduler():
    scheduler.shutdown()
    print("Scheduler encerrado")

@app.get("/check-all")
def check_all_now():
    check_all_prices
    return{"status": "verificação concluída"}

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

@app.get("/")
def root():
    return {"status": "ok", "message": "Price tracker rodando"}

@app.get("/search")
def search(query: str, limit: int = 5):
    results = search_product(query, limit)
    if not results:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado")
    return results

@app.post("/products", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(Product).filter(Product.item_id == product.item_id).first()
    if existing:
        raise HTTPException(status_code = 400, detail = "Produto já cadastrado")
    
    new_product = Product(
        item_id =     product.item_id,
        name =        product.name,
        url=          product.url,
        alert_price=  product.alert_price,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products", response_model=list[ProductResponse])
def list_products(db:Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/products/{product_id}/history")
def get_history(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product). filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail= "Produto não encontrado")
    
    history = (
        db.query(PriceHistory)
        .filter(PriceHistory.product_id == product_id)
        .order_by(PriceHistory.recorded_at.desc())
        .all()
    )
    return {
        "product": product.name,
        "history": [
            {"price": h.price, "recorded_at": h.recorded_at}
            for h in history
        ]
    }

@app.post("/products/{product_id}/check")
def check_price(product_id: int, db:Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not Product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    current_price = get_current_price(product.item_id)
    if current_price is None:
        raise HTTPException(status_code=502, detail="Não foi possível buscar o preço")
    
    entry = PriceHistory(product_id=product.id, price=current_price)
    db.add(entry)
    db.commit()

    alert_triggered = (
        product.alert_price is not None and
        current_price <= product.alert_price
    )

    return {
        "product":     product.name,
        "current_price": current_price,
        "alert_price": product.alert_price,
        "alert_triggered": alert_triggered,
    }