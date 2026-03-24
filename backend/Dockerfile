# Usa uma imagem oficial e leve do Python com base Debian atual
FROM python:3.12-slim-bookworm

# Configurações de runtime e cache para reduzir superfície e ruído operacional
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_DISABLE_PIP_VERSION_CHECK=1 \
	PIP_NO_CACHE_DIR=1 \
	SENTENCE_TRANSFORMERS_HOME=/app/models

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Cria usuário sem privilégios para execução da API
RUN groupadd --system app && useradd --system --gid app --create-home appuser

# Copia o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY backend/requirements.txt ./requirements.txt

# Instala as dependências
RUN pip install -r requirements.txt

# Opcionalmente baixa o modelo durante o build para evitar download no primeiro start.
ARG PRELOAD_MODEL=false
RUN if [ "$PRELOAD_MODEL" = "true" ]; then \
	python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"; \
	fi

# Copia o código do backend
COPY backend/app ./app

# Copia os dados de busca para a imagem (necessário em ambientes sem volume, como Render)
COPY data ./data

# Ajusta permissões e executa como usuário não-root
RUN chown -R appuser:app /app
USER appuser

# Expõe a porta que o FastAPI vai rodar
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]