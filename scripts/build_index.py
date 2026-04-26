import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import TRAIN_CLEAN_PATH, TFIDF_INDEX_PATH
from src.retrieval.tfidf_translator import build_and_save_index


def main():
    print("Construction de l'index TF-IDF...")
    print("Dataset :", TRAIN_CLEAN_PATH)
    print("Sortie  :", TFIDF_INDEX_PATH)

    build_and_save_index(
        csv_path=TRAIN_CLEAN_PATH,
        index_path=TFIDF_INDEX_PATH,
    )

    print("Index TF-IDF construit avec succès.")


if __name__ == "__main__":
    main()