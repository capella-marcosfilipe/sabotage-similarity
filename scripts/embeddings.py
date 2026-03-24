import argparse
import json
from pathlib import Path
from time import perf_counter

import torch
from sentence_transformers import SentenceTransformer


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DEFAULT_INPUT_FILE = DATA_DIR / "letras_chunks.json"
DEFAULT_EMBEDDINGS_FILE = DATA_DIR / "embeddings.pt"
DEFAULT_INDEX_FILE = DATA_DIR / "indice_letras.pt"
DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera embeddings a partir dos chunks e salva artefatos para busca semantica."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_FILE, help="Arquivo JSON de chunks")
    parser.add_argument(
        "--output-embeddings",
        type=Path,
        default=DEFAULT_EMBEDDINGS_FILE,
        help="Arquivo de saida dos embeddings (.pt)",
    )
    parser.add_argument(
        "--output-index",
        type=Path,
        default=DEFAULT_INDEX_FILE,
        help="Arquivo de indice completo (chunks + embeddings)",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL_NAME, help="Modelo SentenceTransformer")
    parser.add_argument("--batch-size", type=int, default=64, help="Tamanho do lote para encode")
    parser.add_argument(
        "--device",
        default=None,
        help="Device do PyTorch (ex.: cpu, cuda). Se omitido, o modelo escolhe automaticamente.",
    )
    parser.add_argument(
        "--normalize",
        action="store_true",
        help="Normaliza embeddings na geracao (util para similaridade por cosseno).",
    )
    return parser.parse_args()


def load_chunks(input_file: Path) -> list[dict]:
    with input_file.open("r", encoding="utf-8") as file:
        chunks = json.load(file)

    if not chunks:
        raise ValueError("O arquivo de chunks esta vazio.")

    if "texto" not in chunks[0]:
        raise KeyError("Estrutura invalida: cada item precisa conter a chave 'texto'.")

    return chunks


def main() -> None:
    args = parse_args()

    args.output_embeddings.parent.mkdir(parents=True, exist_ok=True)
    args.output_index.parent.mkdir(parents=True, exist_ok=True)

    print(f"Carregando modelo: {args.model}")
    model = SentenceTransformer(args.model, device=args.device)

    print(f"Lendo chunks de: {args.input}")
    chunks_data = load_chunks(args.input)
    textos_para_embedding = [item["texto"] for item in chunks_data]

    print(f"Gerando embeddings para {len(textos_para_embedding)} chunks...")
    started_at = perf_counter()
    corpus_embeddings = model.encode(
        textos_para_embedding,
        convert_to_tensor=True,
        batch_size=args.batch_size,
        show_progress_bar=True,
        normalize_embeddings=args.normalize,
    )
    elapsed = perf_counter() - started_at

    # Salvar em CPU melhora portabilidade entre ambientes com/sem GPU.
    corpus_embeddings = corpus_embeddings.cpu()

    print(f"Salvando embeddings em: {args.output_embeddings}")
    torch.save(corpus_embeddings, args.output_embeddings)

    print(f"Salvando indice completo em: {args.output_index}")
    torch.save(
        {
            "chunks_data": chunks_data,
            "embeddings": corpus_embeddings,
            "model_name": args.model,
            "normalize_embeddings": args.normalize,
        },
        args.output_index,
    )

    print(f"Concluido em {elapsed:.2f}s.")


if __name__ == "__main__":
    main()