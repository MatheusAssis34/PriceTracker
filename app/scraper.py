import httpx 
from typing import Optional

FAKE_STORE_SEARCH_URL = "https://fakestoreapi.com/products"
FAKE_STORE_ITEM_URL   = "https://fakestoreapi.com/products/{item_id}"

def search_product(query: str, limit: int = 5) -> list[dict]:
    headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = httpx.get(FAKE_STORE_SEARCH_URL, timeout=10.0)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data:
        if query.lower() in item["title"].lower():
            results.append({
                "item_id": str(item["id"]),
                "name":    item["title"],
                "price":   item["price"],
                "url":     f"https://fakestoreapi.com/products/{item['id']}",
            })
        if len(results) >= limit:
             break

    return results
    
def get_current_price(item_id: str) -> Optional[float]:
        
        headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
        url=FAKE_STORE_ITEM_URL.format(item_id=item_id)
        try:
            response = httpx.get(url, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            return float(data['price'])
        
        except httpx.HTTPSStatusError as e:
            print(f"Erro ao buscar item {item_id}: status {e.respose.status_code}")
            return None
        
        except httpx.RequestError as e:
            print(f"Erro de conexão ao buscar item {item_id}: {e}")
            return None
