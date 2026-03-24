# Scripts para tarefas auxiliares

## Construção de chunks

Lê `data/letras_raw.json`, quebra cada letra em chunks com overlap de 20 palavras, 100 palavras por chunk, e salva em `data/letras_chunks.json`.

Uso:

```bash
python scripts/build_chunks.py
```

Cada chunk tem a seguinte estrutura:

```json
{
    "chunk_id": 0,          # id único global
    "chunk_index": 0,       # posição dentro da música
    "titulo": "Título da Música",
    "url": "URL da letra",
    "texto": "Texto do chunk"
}
```

## Geração de embeddings

Gera embeddings a partir de `data/letras_chunks.json` e salva:

- `data/embeddings.pt`
- `data/indice_letras.pt`

Uso padrao:

```bash
python scripts/embeddings.py
```

Uso customizado:

```bash
python scripts/embeddings.py --input data/letras_chunks.json --output-embeddings data/embeddings.pt --output-index data/indice_letras.pt --batch-size 64 --normalize
```
