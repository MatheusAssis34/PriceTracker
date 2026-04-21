from app.database import create_tables, SessionLocal
from app.models import Product

create_tables()

db = SessionLocal()
produto_teste = Product(
    name="Teclado Mecânico",
    url="https//www.mercadolivre.com.br/...",
    item_id="MLB123456"
)

db.add(produto_teste)
db.commit()
print("Banco criado e produto inserido com sucesso")
db.close()