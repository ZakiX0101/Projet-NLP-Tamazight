import sys
from pathlib import Path
from difflib import SequenceMatcher

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import TEST_CLEAN_PATH
from src.retrieval.tfidf_translator import TfidfTranslator
from src.preprocessing.normalization import normalize_text


def string_similarity(a: str, b: str) -> float:
    a = normalize_text(a)
    b = normalize_text(b)

    if not a or not b:
        return 0.0

    return SequenceMatcher(None, a, b).ratio()


def main():
    df = pd.read_csv(TEST_CLEAN_PATH)
    df = df[["tamazight", "arabic"]].dropna()

    translator = TfidfTranslator()
    translator.load()

    total = len(df)
    reliable_count = 0
    exact_match_count = 0
    avg_retrieval_score = 0.0
    avg_text_similarity = 0.0

    examples = []

    for _, row in df.iterrows():
        src = row["tamazight"]
        ref = row["arabic"]

        result = translator.translate(src)

        pred = result.translation
        sim = string_similarity(pred, ref)

        if result.reliable:
            reliable_count += 1

        if normalize_text(pred) == normalize_text(ref):
            exact_match_count += 1

        avg_retrieval_score += result.score
        avg_text_similarity += sim

        if len(examples) < 10:
            examples.append(
                {
                    "source": src,
                    "reference": ref,
                    "prediction": pred,
                    "score": result.score,
                    "similarity": sim,
                    "reliable": result.reliable,
                }
            )

    avg_retrieval_score /= total
    avg_text_similarity /= total

    print("=" * 80)
    print("Évaluation TF-IDF")
    print("=" * 80)
    print("Nombre total :", total)
    print("Traductions fiables :", reliable_count)
    print("Taux fiable :", round(reliable_count / total * 100, 2), "%")
    print("Exact match :", exact_match_count)
    print("Exact match rate :", round(exact_match_count / total * 100, 2), "%")
    print("Score TF-IDF moyen :", round(avg_retrieval_score, 4))
    print("Similarité texte moyenne :", round(avg_text_similarity, 4))

    print("\nExemples :")
    for ex in examples:
        print("-" * 80)
        print("Source     :", ex["source"])
        print("Référence  :", ex["reference"])
        print("Prédiction :", ex["prediction"])
        print("Score      :", round(ex["score"], 4))
        print("Similarité :", round(ex["similarity"], 4))
        print("Fiable     :", ex["reliable"])


if __name__ == "__main__":
    main()