from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.models import Product, PriceHistory
from app.scraper import get_current_price
from datetime import datetime, timezone

def check_all_prices():
    print(f"[{datetime.now()}]Verificando preços...")

    db = SessionLocal()
    try:
        products = db.query(Product).all()

        if not products:
            print("Nenhum produto cadastrado ainda")
            return
        for product in products:
            price = get_current_price(product.item_id)

            if price is None:
                print(f" Não foi possível buscar preço de: {product.name}")
                continue

            entry = PriceHistory(
                product_id = product.id,
                price=price
            )
            db.add(entry)
            db.commit()
            
            print(f" {product.name[:40]} => $ {price:.2f}")

            if product.alert_price and price <= product.alert_price:
                print(f" ALERTA: preço abaixo de $ {product.alert_price:.2f}!")
    finally:
        db.close()

scheduler = BackgroundScheduler()

scheduler.add_job(
    check_all_prices,
    trigger="interval",
    hours=1,
    id="price_check",
    replace_existing=True
)