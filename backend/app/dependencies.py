from functools import lru_cache

from .config import DATA_DIR, MODEL_NAME
from .services.similarity_service import SimilarityService


@lru_cache
def get_similarity_service() -> SimilarityService:
    return SimilarityService(model_name=MODEL_NAME, data_dir=DATA_DIR)
