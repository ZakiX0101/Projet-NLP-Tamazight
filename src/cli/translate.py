import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.retrieval.tfidf_translator import TfidfTranslator


def main():
    parser = argparse.ArgumentParser(
        description="Traduction Tamazight/Tifinagh vers Arabe avec TF-IDF"
    )

    parser.add_argument(
        "--text",
        type=str,
        required=True,
        help="Texte Tamazight/Tifinagh à traduire",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Nombre d'alternatives à afficher",
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.35,
        help="Seuil minimum de similarité",
    )

    args = parser.parse_args()

    translator = TfidfTranslator(
        min_similarity=args.threshold,
        top_k=args.top_k,
    )
    translator.load()

    result = translator.translate(
        args.text,
        top_k=args.top_k,
        min_similarity=args.threshold,
    )

    print("=" * 80)
    print("Texte saisi       :", result.query)
    print("Texte normalisé   :", result.normalized_query)
    print("Score             :", round(result.score, 4))
    print("Fiable            :", "Oui" if result.reliable else "Non")

    if result.reliable:
        print("Traduction        :", result.translation)
        print("Source trouvée    :", result.matched_source)
    else:
        print("Traduction        : Aucune traduction fiable trouvée.")
        print("Source la plus proche :", result.matched_source)

    print("=" * 80)
    print("Alternatives :")

    for i, candidate in enumerate(result.alternatives, start=1):
        print(f"\n{i}. Score : {candidate.score:.4f}")
        print("Source     :", candidate.source)
        print("Traduction :", candidate.translation)


if __name__ == "__main__":
    main()