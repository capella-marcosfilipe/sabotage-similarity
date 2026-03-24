# Frontend

Frontend da aplicacao de pesquisa por similaridade com LLM.

## Como funciona

O frontend e uma pagina estatica servida por Nginx. A API pode ser acessada de duas formas:

- Modo padrao (recomendado): usa `/api` e deixa o Nginx fazer proxy para o backend.
- Modo externo: define `API_BASE_URL` para apontar para uma API publica.

## Execucao local

Na raiz do projeto:

```bash
docker compose up --build
```

Depois abra:

- Frontend: <http://localhost:8080>

## Deploy

As instrucoes de deploy no Render foram movidas para `RENDER_DEPLOY.md` na raiz do projeto.

## Arquivos importantes

- `Dockerfile`: imagem Nginx do frontend
- `nginx.conf`: proxy `/api` e health endpoint
- `docker-entrypoint.sh`: gera `config.js` com variaveis de ambiente
- `config.template.js`: template da configuracao em runtime
