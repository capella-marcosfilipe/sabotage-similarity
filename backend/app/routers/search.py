from fastapi import APIRouter, Depends

from ..dependencies import get_similarity_service
from ..schemas import QueryRequest, SearchResponse
from ..services.similarity_service import SimilarityService


router = APIRouter(tags=["Busca"])


@router.post("/buscar", response_model=SearchResponse)
def buscar_similaridade(
    request: QueryRequest,
    service: SimilarityService = Depends(get_similarity_service),
) -> SearchResponse:
    resultados = service.search(request.texto, request.top_k)
    return SearchResponse(resultados=resultados)
