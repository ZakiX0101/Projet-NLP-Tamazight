import re
import unicodedata


ZERO_WIDTH_CHARS = [
    "\u200b",
    "\u200c",
    "\u200d",
    "\ufeff",
]


def normalize_text(text: str) -> str:
    """
    Normalisation générale du texte.
    """
    if text is None:
        return ""

    text = str(text)
    text = unicodedata.normalize("NFKC", text)

    for char in ZERO_WIDTH_CHARS:
        text = text.replace(char, "")

    text = text.strip()
    text = re.sub(r"\s+", " ", text)

    return text


def normalize_tamazight(text: str) -> str:
    """
    Normalisation spécifique pour le texte Tamazight/Tifinagh.
    """
    text = normalize_text(text)

    replacements = {
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "،": ",",
        "؛": ";",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_arabic(text: str) -> str:
    """
    Normalisation légère de l'arabe.
    """
    text = normalize_text(text)

    replacements = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ى": "ي",
        "ة": "ه",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\s+", " ", text).strip()
    return text


def tifinagh_ratio(text: str) -> float:
    """
    Calcule le pourcentage de caractères Tifinagh dans un texte.
    """
    text = normalize_text(text)
    chars = [c for c in text if not c.isspace()]

    if not chars:
        return 0.0

    tif = sum(1 for c in chars if "\u2d30" <= c <= "\u2d7f")
    return tif / len(chars)


def arabic_ratio(text: str) -> float:
    """
    Calcule le pourcentage de caractères arabes dans un texte.
    """
    text = normalize_text(text)
    chars = [c for c in text if not c.isspace()]

    if not chars:
        return 0.0

    ar = sum(
        1
        for c in chars
        if "\u0600" <= c <= "\u06ff"
        or "\u0750" <= c <= "\u077f"
        or "\u08a0" <= c <= "\u08ff"
    )

    return ar / len(chars)