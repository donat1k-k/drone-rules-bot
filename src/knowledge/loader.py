import yaml
from pathlib import Path

_TOPICS_DIR = Path(__file__).parent.parent.parent / "data" / "topics"
_cache: dict[str, dict] = {}


def load_topic(topic_id: str) -> dict:
    if topic_id not in _cache:
        path = _TOPICS_DIR / f"{topic_id}.yaml"
        with open(path, encoding="utf-8") as f:
            _cache[topic_id] = yaml.safe_load(f)
    return _cache[topic_id]
