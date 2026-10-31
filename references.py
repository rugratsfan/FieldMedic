from pathlib import Path
import re

REFERENCE_FOLDER = Path(__file__).parent / "references"


def tokenize(text):
    return set(
        re.findall(r"[a-zA-Z0-9]+", text.lower())
    )


def search_references(query, maximum_results=3):
    if not REFERENCE_FOLDER.exists():
        return []

    query_words = tokenize(query)

    if not query_words:
        return []

    matches = []

    for file_path in REFERENCE_FOLDER.glob("*.txt"):
        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore"
            )
        except OSError:
            continue

        content_words = tokenize(content)
        score = len(query_words.intersection(content_words))

        if score > 0:
            matches.append({
                "source": file_path.name,
                "score": score,
                "content": content[:3000]
            })

    matches.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return matches[:maximum_results]


def format_references(matches):
    if not matches:
        return (
            "No matching local reference was found. "
            "Do not invent reference claims."
        )

    formatted = []

    for match in matches:
        formatted.append(
            f"SOURCE: {match['source']}\n"
            f"{match['content']}"
        )

    return "\n\n".join(formatted)