import os
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_DIR.parent

DEFAULT_DATA_DIR = Path("/app/data") if Path("/app/data").exists() else REPO_ROOT / "data"
DATA_DIR = Path(os.getenv("DATA_DIR", str(DEFAULT_DATA_DIR)))
MODEL_NAME = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
TOP_K_DEFAULT = int(os.getenv("TOP_K_DEFAULT", "3"))
TOP_K_MAX = int(os.getenv("TOP_K_MAX", "20"))


def _parse_csv_env(var_name: str, default: str) -> list[str]:
	raw_value = os.getenv(var_name, default)
	return [item.strip() for item in raw_value.split(",") if item.strip()]


APP_ENV = os.getenv("APP_ENV", "development")
CORS_ALLOW_ORIGINS = _parse_csv_env("CORS_ALLOW_ORIGINS", "*")
TRUSTED_HOSTS = _parse_csv_env("TRUSTED_HOSTS", "*")
