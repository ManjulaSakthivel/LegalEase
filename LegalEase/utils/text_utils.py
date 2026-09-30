import re


def sanitize_text(text: str) -> str:
    """Normalize text for predictable exports, especially PDF output."""
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
        "\u2022": "-",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # fpdf's core fonts are Latin-1 oriented. Replace remaining unsupported
    # characters rather than producing a broken PDF.
    text = text.encode("latin-1", errors="replace").decode("latin-1")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def terms_from_text(terms: str) -> list[str]:
    return [item.strip() for item in terms.split(";") if item.strip()]
