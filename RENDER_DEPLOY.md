# Deploy no Render

Este guia concentra os passos para publicar o projeto no Render usando os Dockerfiles ja criados.

## Visao geral

Como o Render nao usa docker-compose para Web Service, publique em dois servicos:

- Backend: API FastAPI
- Frontend: pagina estatica Nginx

## 1) Preparar repositorio

1. Suba o codigo para o GitHub.
2. Garanta que os dados usados pelo backend estao disponiveis no build/runtime do servico backend.
3. Confirme que o backend sobe com `backend/Dockerfile` e o frontend com `frontend/Dockerfile`.

## 2) Criar servico do backend no Render

1. Acesse Render Dashboard -> New + -> Web Service.
2. Conecte o repositorio GitHub.
3. Configure:

- Name: sabotage-backend
- Environment: Docker
- Root Directory: backend
- Branch: branch principal
- Plan: Free

4. Defina variaveis de ambiente:

- APP_ENV=production
- DATA_DIR=/app/data
- CORS_ALLOW_ORIGINS=*
- TRUSTED_HOSTS=*

5. Crie o servico e aguarde deploy.
6. Teste o healthcheck publico:

- https://SEU_BACKEND.onrender.com/health

## 3) Criar servico do frontend no Render

1. Render Dashboard -> New + -> Web Service.
2. Mesmo repositorio GitHub.
3. Configure:

- Name: sabotage-frontend
- Environment: Docker
- Root Directory: frontend
- Branch: branch principal
- Plan: Free

4. Defina variavel de ambiente:

- API_BASE_URL=https://SEU_BACKEND.onrender.com

Importante: nao coloque `/buscar` no final dessa URL.

5. Crie o servico e aguarde deploy.
6. Abra a URL publica do frontend e valide a busca.

## 4) Pos-deploy recomendado

1. Trocar CORS_ALLOW_ORIGINS de `*` para a URL real do frontend.
2. Trocar TRUSTED_HOSTS de `*` para o host publico esperado.
3. Verificar logs dos dois servicos no painel do Render.
4. Se houver cold start no plano Free, considerar plano pago para reduzir latencia.
