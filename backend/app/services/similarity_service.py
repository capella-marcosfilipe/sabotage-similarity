import json
from pathlib import Path

import torch
from sentence_transformers import SentenceTransformer, util


class SimilarityService:
    def __init__(self, model_name: str, data_dir: Path) -> None:
        self.model_name = model_name
        self.data_dir = data_dir

        self.model = SentenceTransformer(self.model_name)
        self.chunks_data = self._load_chunks()
        self.corpus_embeddings = self._load_embeddings()

    def _load_chunks(self) -> list[dict]:
        chunks_path = self.data_dir / "letras_chunks.json"
        with chunks_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _load_embeddings(self):
        embeddings_path = self.data_dir / "embeddings.pt"
        try:
            return torch.load(embeddings_path, weights_only=True)
        except TypeError:
            return torch.load(embeddings_path)

    def search(self, texto: str, top_k: int) -> list[dict]:
        query_embedding = self.model.encode(texto, convert_to_tensor=True)
        hits = util.semantic_search(query_embedding, self.corpus_embeddings, top_k=top_k)[0]

        results: list[dict] = []
        for hit in hits:
            corpus_id = int(hit["corpus_id"])
            chunk = self.chunks_data[corpus_id]
            results.append(
                {
                    "titulo": chunk["titulo"],
                    "trecho": chunk["texto"],
                    "url": chunk["url"],
                    "score": round(float(hit["score"]), 4),
                }
            )
        return results
