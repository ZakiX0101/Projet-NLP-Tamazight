from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"

TRAIN_CLEAN_PATH = PROCESSED_DIR / "train_clean.csv"
VALID_CLEAN_PATH = PROCESSED_DIR / "valid_clean.csv"
TEST_CLEAN_PATH = PROCESSED_DIR / "test_clean.csv"

MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

TFIDF_INDEX_PATH = MODELS_DIR / "tfidf_translation_memory.joblib"

SOURCE_COLUMN = "tamazight"
TARGET_COLUMN = "arabic"

DEFAULT_TOP_K = 5
DEFAULT_MIN_SIMILARITY = 0.35

TFIDF_PARAMS = {
    "analyzer": "char_wb",
    "ngram_range": (2, 6),
    "lowercase": False,
    "min_df": 1,
    "max_features": 300_000,
}