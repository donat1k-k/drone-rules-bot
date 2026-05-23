from __future__ import annotations

from src.knowledge.loader import load_topic

_TOPIC_IDS = [
    "preparation", "safety", "restricted_zones", "registration",
    "signal_loss", "tips", "faq", "links",
]

_STOP_WORDS = {
    "что", "как", "где", "когда", "зачем", "почему", "можно", "нельзя",
    "нужно", "надо", "мне", "меня", "тебе", "тебя", "я", "у", "в", "на",
    "с", "и", "или", "а", "но", "для", "по", "при", "не", "это", "бот",
    "ли", "если", "то", "бы", "же", "ещё", "уже", "так", "там", "тут",
    "он", "она", "они", "мы", "вы", "его", "её", "их", "нам", "вам",
    "будет", "было", "быть", "есть", "был", "была", "ведь", "даже",
}


def _word_in_text(word: str, text: str) -> bool:
    if word in text:
        return True
    # prefix match handles basic Russian morphology (регистрировать → регис… matches регистрация)
    if len(word) >= 5 and word[:5] in text:
        return True
    return False


def search_knowledge(query: str) -> dict | None:
    """Return best-matching topic or None if no confident match (score < 2.0)."""
    query_lower = query.lower()
    words = {
        w for w in query_lower.split()
        if len(w) >= 4 and w not in _STOP_WORDS
    }
    if not words:
        return None

    best_score = 0.0
    best_topic = None

    for topic_id in _TOPIC_IDS:
        topic = load_topic(topic_id)
        kw_text = " ".join(topic.get("keywords", [])).lower()
        title_text = topic.get("title", "").lower()
        body_text = topic.get("body", "").lower()

        score = 0.0
        for word in words:
            if _word_in_text(word, kw_text):
                score += 2.0
            elif _word_in_text(word, title_text):
                score += 1.0
            elif _word_in_text(word, body_text):
                score += 0.5

        if score > best_score:
            best_score = score
            best_topic = topic

    return best_topic if best_score >= 2.0 else None
