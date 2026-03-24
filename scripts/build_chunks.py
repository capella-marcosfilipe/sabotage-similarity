import json
from pathlib import Path


# ── Settings ────────────────────────────────────────────────
DATA_DIR    = Path(__file__).parent.parent / "data"
INPUT_FILE  = DATA_DIR / "letras_raw.json"
OUTPUT_FILE = DATA_DIR / "letras_chunks.json"

CHUNK_SIZE  = 100
OVERLAP     = 20
# ────────────────────────────────────────────────────────────────


def make_chunks(texto: str, chunk_size: int, overlap: int) -> list[str]:
    """
    Quebra um texto em chunks de `chunk_size` palavras
    com `overlap` palavras de sobreposição entre chunks consecutivos.
    """
    palavras = texto.split()
    chunks = []
    inicio = 0

    while inicio < len(palavras):
        fim = inicio + chunk_size
        chunk = " ".join(palavras[inicio:fim])
        chunks.append(chunk)

        # Se já chegou no fim, para
        if fim >= len(palavras):
            break

        # Avança (chunk_size - overlap) pra criar a sobreposição
        inicio += chunk_size - overlap

    return chunks


def main():
    # Lê o JSON com as letras
    with open(INPUT_FILE, encoding="utf-8") as f:
        letras = json.load(f)

    print(f"Letras carregadas: {len(letras)}")

    todos_chunks = []
    total_chunks = 0

    for musica in letras:
        titulo = musica["titulo"]
        url    = musica["url"]
        letra  = musica["letra"]

        chunks = make_chunks(letra, CHUNK_SIZE, OVERLAP)

        for i, chunk in enumerate(chunks):
            todos_chunks.append({
                "chunk_id": total_chunks,
                "chunk_index": i,
                "titulo": titulo,
                "url": url,
                "texto": chunk,
            })
            total_chunks += 1

        print(f"  '{titulo}': {len(chunks)} chunks")

    # Salva o resultado
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(todos_chunks, f, ensure_ascii=False, indent=2)

    print(f"\nTotal de chunks gerados: {total_chunks}")
    print(f"Salvo em: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    