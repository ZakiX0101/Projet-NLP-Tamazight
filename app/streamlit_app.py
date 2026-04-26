import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import TRAIN_CLEAN_PATH, TFIDF_INDEX_PATH
from src.retrieval.tfidf_translator import TfidfTranslator, build_and_save_index


st.set_page_config(
    page_title="Traducteur Tamazight → Arabe",
    page_icon="ⵣ",
    layout="wide",
)


@st.cache_resource
def load_translator():
    if not TFIDF_INDEX_PATH.exists():
        build_and_save_index(TRAIN_CLEAN_PATH, TFIDF_INDEX_PATH)

    translator = TfidfTranslator()
    translator.load()
    return translator


@st.cache_data
def load_examples():
    if TRAIN_CLEAN_PATH.exists():
        df = pd.read_csv(TRAIN_CLEAN_PATH)
        df = df[["tamazight", "arabic"]].dropna()
        return df.sample(min(10, len(df)), random_state=42)
    return pd.DataFrame(columns=["tamazight", "arabic"])


def main():
    st.title("ⵣ Traducteur Tamazight / Tifinagh → Arabe")
    st.caption("Système de traduction basé sur TF-IDF + similarité cosinus")

    translator = load_translator()

    with st.sidebar:
        st.header("Paramètres")

        threshold = st.slider(
            "Seuil de similarité",
            min_value=0.0,
            max_value=1.0,
            value=0.35,
            step=0.05,
        )

        top_k = st.slider(
            "Nombre d'alternatives",
            min_value=1,
            max_value=10,
            value=5,
            step=1,
        )

        st.markdown("---")
        st.write("Index utilisé :")
        st.code(str(TFIDF_INDEX_PATH))

        if st.button("Reconstruire l'index TF-IDF"):
            build_and_save_index(TRAIN_CLEAN_PATH, TFIDF_INDEX_PATH)
            st.cache_resource.clear()
            st.success("Index reconstruit. Recharge la page si nécessaire.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Texte source")

        text = st.text_area(
            "Entrez un texte en Tamazight/Tifinagh",
            height=160,
            placeholder="Exemple : ⵜⴳⴰ ⵜⴰⵖⴰⵔⴰⵙⵜ ⵜⴰⵔⵎⵉⴷⵉⵜ",
        )

        translate_button = st.button("Traduire", type="primary")

    with col2:
        st.subheader("Résultat")

        if translate_button:
            if not text.strip():
                st.warning("Veuillez entrer un texte.")
            else:
                result = translator.translate(
                    text,
                    top_k=top_k,
                    min_similarity=threshold,
                )

                if result.reliable:
                    st.success(result.translation)
                else:
                    st.warning("Aucune traduction fiable trouvée.")
                    st.info(
                        "Le système a trouvé une phrase proche, "
                        "mais le score est inférieur au seuil choisi."
                    )

                st.metric("Score de similarité", f"{result.score:.4f}")

                st.write("Phrase la plus proche trouvée :")
                st.code(result.matched_source)

                st.write("Texte normalisé :")
                st.code(result.normalized_query)

                st.markdown("### Alternatives")

                alternatives_df = pd.DataFrame(
                    [
                        {
                            "score": round(c.score, 4),
                            "source": c.source,
                            "traduction": c.translation,
                        }
                        for c in result.alternatives
                    ]
                )

                st.dataframe(alternatives_df, use_container_width=True)

    st.markdown("---")
    st.subheader("Exemples depuis la base")

    examples = load_examples()

    if not examples.empty:
        st.dataframe(examples, use_container_width=True)


if __name__ == "__main__":
    main()