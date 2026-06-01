# PriceTracker

Price Tracker API
API REST para rastreamento automático de preços de produtos, construída com FastAPI e SQLite.

Sobre o projeto
O Price Tracker monitora preços de produtos de forma autônoma. Você cadastra um produto, define um preço alvo, e o sistema verifica automaticamente a cada hora se o preço caiu. Todo o histórico fica salvo no banco de dados e pode ser consultado a qualquer momento via API.
Projeto desenvolvido como portfólio para demonstrar conhecimentos em Python, APIs REST, banco de dados relacional e consumo de APIs externas.




Tecnologias utilizadas:

Python 3.12,
FastAPI — framework para construção da API REST,
SQLAlchemy — ORM para comunicação com o banco de dados,
SQLite — banco de dados relacional local,
httpx — cliente HTTP para consumo de APIs externas,
APScheduler — agendamento de tarefas em background,
Uvicorn — servidor ASGI para rodar a aplicação




Como rodar localmente
1. Clone o repositório
bashgit clone https://github.com/seu-usuario/price-tracker.git
cd price-tracker
2. Crie e ative o ambiente virtual
bashpython -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux / macOS
3. Instale as dependências
bashpip install -r requirements.txt
4. Rode a aplicação
bashuvicorn app.main:app --reload
A API estará disponível em http://localhost:8000.
A documentação interativa estará disponível em http://localhost:8000/docs.

Endpoints
MétodoRotaDescriçãoGET/Verifica se a API está no arGET/search?query={}Busca produtos pelo nomePOST/productsCadastra um produto para rastrearGET/productsLista todos os produtos cadastradosPOST/products/{id}/checkBusca e salva o preço atual do produtoGET/products/{id}/historyRetorna o histórico de preçosGET/check-allDispara verificação manual em todos os produtos

Exemplo de uso
Buscar um produto
bashcurl http://localhost:8000/search?query=gold
Resposta:
json[
  {
    "item_id": "5",
    "name": "John Hardy Women's Legends Naga Gold & Silver Dragon Station Chain Bracelet",
    "price": 695.0,
    "url": "https://fakestoreapi.com/products/5"
  }
]
Cadastrar um produto para rastrear
bashcurl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": "5",
    "name": "John Hardy Women'\''s Legends Naga Gold",
    "url": "https://fakestoreapi.com/products/5",
    "alert_price": 600.00
  }'
Consultar histórico de preços
bashcurl http://localhost:8000/products/1/history
Resposta:
json{
  "product": "John Hardy Women's Legends Naga Gold",
  "history": [
    {
      "price": 695.0,
      "recorded_at": "2026-05-01T13:52:49.720629"
    }
  ]
}

Decisões técnicas
Por que FastAPI?
FastAPI gera documentação interativa automaticamente via Swagger UI, tem validação de dados nativa com Pydantic e é um dos frameworks Python mais adotados no mercado atualmente.
Por que SQLite?
Para um projeto de portfólio e uso local, SQLite elimina a necessidade de configurar um servidor de banco de dados externo. A troca para PostgreSQL em produção exigiria mudar apenas a string de conexão no database.py.
Por que APScheduler?
Permite rodar tarefas periódicas em background sem depender de ferramentas externas como cron ou Celery, mantendo o projeto simples e autocontido.
Por que httpx em vez de requests?
httpx é a evolução moderna do requests, com suporte nativo a requisições assíncronas e uma API muito similar, facilitando uma eventual migração para endpoints async no futuro.

<img width="1631" height="903" alt="Captura de tela 2026-05-03 195917" src="https://github.com/user-attachments/assets/85b59ee6-b828-47fa-9147-0e03d7d9399d" />
