from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from src.config import (
    SOURCE_COLUMN,
    TARGET_COLUMN,
    TFIDF_INDEX_PATH,
    TFIDF_PARAMS,
    DEFAULT_MIN_SIMILARITY,
    DEFAULT_TOP_K,
)
from src.preprocessing.normalization import normalize_tamazight, normalize_text


@dataclass
class TranslationCandidate:
    source: str
    translation: str
    score: float


@dataclass
class TranslationResult:
    query: str
    normalized_query: str
    translation: str
    score: float
    matched_source: str
    reliable: bool
    alternatives: List[TranslationCandidate]


class TfidfTranslator:
    def __init__(
        self,
        index_path: Path = TFIDF_INDEX_PATH,
        min_similarity: float = DEFAULT_MIN_SIMILARITY,
        top_k: int = DEFAULT_TOP_K,
    ):
        self.index_path = Path(index_path)
        self.min_similarity = min_similarity
        self.top_k = top_k

        self.vectorizer: Optional[TfidfVectorizer] = None
        self.matrix = None
        self.sources: List[str] = []
        self.targets: List[str] = []
        self.normalized_sources: List[str] = []
        self.exact_lookup = {}

    def build_from_csv(
        self,
        csv_path: Path,
        source_col: str = SOURCE_COLUMN,
        target_col: str = TARGET_COLUMN,
    ) -> None:
        csv_path = Path(csv_path)

        if not csv_path.exists():
            raise FileNotFoundError(f"Fichier introuvable : {csv_path}")

        df = pd.read_csv(csv_path)

        if source_col not in df.columns or target_col not in df.columns:
            raise ValueError(
                f"Colonnes attendues : {source_col}, {target_col}. "
                f"Colonnes trouvées : {list(df.columns)}"
            )

        df = df[[source_col, target_col]].dropna()
        df[source_col] = df[source_col].astype(str).map(normalize_tamazight)
        df[target_col] = df[target_col].astype(str).map(normalize_text)

        df = df[(df[source_col] != "") & (df[target_col] != "")]
        df = df.drop_duplicates(subset=[source_col, target_col])

        # Si même phrase source avec plusieurs traductions, on garde la première.
        df = df.drop_duplicates(subset=[source_col], keep="first")

        self.sources = df[source_col].tolist()
        self.targets = df[target_col].tolist()
        self.normalized_sources = [normalize_tamazight(x) for x in self.sources]

        self.vectorizer = TfidfVectorizer(**TFIDF_PARAMS)
        self.matrix = self.vectorizer.fit_transform(self.normalized_sources)

        self.exact_lookup = {
            src: (original, tgt)
            for src, original, tgt in zip(
                self.normalized_sources,
                self.sources,
                self.targets,
            )
        }

    def save(self, path: Optional[Path] = None) -> None:
        path = Path(path or self.index_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "vectorizer": self.vectorizer,
            "matrix": self.matrix,
            "sources": self.sources,
            "targets": self.targets,
            "normalized_sources": self.normalized_sources,
            "exact_lookup": self.exact_lookup,
            "min_similarity": self.min_similarity,
            "top_k": self.top_k,
        }

        joblib.dump(payload, path)

    def load(self, path: Optional[Path] = None) -> None:
        path = Path(path or self.index_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Index TF-IDF introuvable : {path}. "
                "Lance d'abord : python scripts/build_index.py"
            )

        payload = joblib.load(path)

        self.vectorizer = payload["vectorizer"]
        self.matrix = payload["matrix"]
        self.sources = payload["sources"]
        self.targets = payload["targets"]
        self.normalized_sources = payload["normalized_sources"]
        self.exact_lookup = payload["exact_lookup"]
        self.min_similarity = payload.get("min_similarity", self.min_similarity)
        self.top_k = payload.get("top_k", self.top_k)

    def translate(
        self,
        text: str,
        top_k: Optional[int] = None,
        min_similarity: Optional[float] = None,
    ) -> TranslationResult:
        if self.vectorizer is None or self.matrix is None:
            self.load()

        top_k = top_k or self.top_k
        min_similarity = (
            self.min_similarity if min_similarity is None else min_similarity
        )

        query = str(text)
        normalized_query = normalize_tamazight(query)

        if normalized_query == "":
            return TranslationResult(
                query=query,
                normalized_query=normalized_query,
                translation="",
                score=0.0,
                matched_source="",
                reliable=False,
                alternatives=[],
            )

        # Correspondance exacte
        if normalized_query in self.exact_lookup:
            matched_source, translation = self.exact_lookup[normalized_query]

            return TranslationResult(
                query=query,
                normalized_query=normalized_query,
                translation=translation,
                score=1.0,
                matched_source=matched_source,
                reliable=True,
                alternatives=[
                    TranslationCandidate(
                        source=matched_source,
                        translation=translation,
                        score=1.0,
                    )
                ],
            )

        query_vec = self.vectorizer.transform([normalized_query])
        similarities = linear_kernel(query_vec, self.matrix).ravel()

        if len(similarities) == 0:
            return TranslationResult(
                query=query,
                normalized_query=normalized_query,
                translation="",
                score=0.0,
                matched_source="",
                reliable=False,
                alternatives=[],
            )

        top_k = min(top_k, len(similarities))

        # Plus rapide que argsort complet sur gros dataset
        top_indices = np.argpartition(similarities, -top_k)[-top_k:]
        top_indices = top_indices[np.argsort(similarities[top_indices])[::-1]]

        alternatives = []
        for idx in top_indices:
            alternatives.append(
                TranslationCandidate(
                    source=self.sources[idx],
                    translation=self.targets[idx],
                    score=float(similarities[idx]),
                )
            )

        best = alternatives[0]
        reliable = best.score >= min_similarity

        translation = best.translation if reliable else ""

        return TranslationResult(
            query=query,
            normalized_query=normalized_query,
            translation=translation,
            score=best.score,
            matched_source=best.source,
            reliable=reliable,
            alternatives=alternatives,
        )


def build_and_save_index(csv_path: Path, index_path: Path = TFIDF_INDEX_PATH) -> None:
    translator = TfidfTranslator(index_path=index_path)
    translator.build_from_csv(csv_path)
    translator.save(index_path)