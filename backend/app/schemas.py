from pydantic import BaseModel, Field

from .config import TOP_K_DEFAULT, TOP_K_MAX


class QueryRequest(BaseModel):
    texto: str = Field(
        ...,
        min_length=1,
        description="Texto da consulta para busca semantica.",
        examples=["Como e a dura realidade e a sobrevivencia nas ruas do Brooklin?"],
    )
    top_k: int = Field(
        default=TOP_K_DEFAULT,
        ge=1,
        le=TOP_K_MAX,
        description=(
            "Quantidade de resultados mais similares retornados. "
            "Ex.: top_k=3 retorna os 3 trechos com maior score de similaridade."
        ),
        examples=[3],
    )


class SearchResult(BaseModel):
    titulo: str
    trecho: str
    url: str
    score: float


class SearchResponse(BaseModel):
    resultados: list[SearchResult]
