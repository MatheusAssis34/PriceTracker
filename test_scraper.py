from app.scraper import search_product, get_current_price

print("=== Resultados da busca ===")
resultados = search_product("gold", limit=3)
for r in resultados:
    print(f"{r['item_id']} | $ {r['price']:.2f} | {r['name'][:50]}")

primeiro_id = resultados[0]["item_id"]
print(f"\n=== Preço atual do item {primeiro_id} ===")
preco = get_current_price(primeiro_id)
print(f"$ {preco:.2f}")