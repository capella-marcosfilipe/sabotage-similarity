# Backend - API de Busca por Similaridade

Esta API expõe um endpoint FastAPI para busca semântica em letras usando Sentence Transformers.

## Arquitetura (simples)

```text
backend/
  app/
    main.py                   # criação da aplicação FastAPI
    config.py                 # configurações e paths
    schemas.py                # modelos de request/response
    dependencies.py           # injeção de dependências (service singleton)
    routers/
      search.py               # rota /buscar
    services/
      similarity_service.py   # regra de negócio da busca
```

## Endpoint

- `POST /buscar`
- `GET /health`

Corpo:

```json
{
  "texto": "meu coração não sei por que",
  "top_k": 3
}
```

Resposta:

```json
{
  "resultados": [
    {
      "titulo": "...",
      "trecho": "...",
      "url": "...",
      "score": 0.9123
    }
  ]
}
```

### O que e top_k?

`top_k` define quantos resultados mais parecidos com o texto da consulta a API deve retornar.

- `top_k = 1`: retorna apenas o melhor resultado.
- `top_k = 3`: retorna os 3 melhores resultados.
- Quanto maior o `top_k`, mais resultados voce recebe (ate o limite configurado na API).

Em geral:

- use valores pequenos (1-5) para respostas mais objetivas;
- use valores maiores quando quiser explorar mais trechos relacionados.

## Rodando localmente

No diretório raiz do projeto:

```bash
uv sync
uv run uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Se necessário, defina `DATA_DIR` para apontar para a pasta com `letras_chunks.json` e `embeddings.pt`.

### Variaveis importantes

- `APP_ENV`: ambiente da aplicacao (`development` ou `production`).
- `DATA_DIR`: pasta dos arquivos de dados (json/embeddings).
- `CORS_ALLOW_ORIGINS`: lista separada por virgula para CORS.
- `TRUSTED_HOSTS`: lista separada por virgula para hosts permitidos.

## Rodando com Docker

No diretório raiz do projeto:

```bash
docker compose up --build
```

O volume `./data:/app/data` no `docker-compose.yml` já disponibiliza os dados para a API.
