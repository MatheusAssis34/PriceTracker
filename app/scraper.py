import httpx 
from typing import Optional

MELI_SEARCH_URL = "https://api.mercadolivre.com/sites/MLB/search"
MELI_ITEM_URL  = "https://api.mercadolivre.com/items/{item_id}"

def search_product(query: str, limit: int = 5) -> list[dict]:
    response = httpx.get(MELI_SEARCH_URL, params={"q": query, "limit": limit})
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("results", []):
        results.append({
            "item_id": item["id"],
            "name":    item["title"],
            "price":   item["price"],
            "url":     item["permalink"],
        })

        return results
    
    def get_current_price(item_id: str) -> Optional[float]:
        url=MELI_ITEM_URL.format(item_id=item_id)
        try:
            response = httpx.get(url, timeout=10.0)
            response.raise_for_status()

            data = response.json()

            return float(data['price'])
        
        except httpx.HTTPSstatusError as e:
            print(f"Erro ao buscar item {item_id}: status {e.respose.status_code}")
            return None
        
        except httpx.RequestError as e:
            print(f"Erro de conexão ao buscar item {item_id}: {e}")
            return None
