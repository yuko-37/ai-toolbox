import json
import logging
from pathlib import Path
from datetime import datetime
from dataprovider import get_titles

PROJECT_ROOT = Path(__file__).resolve().parents[1]
_SHOWS_PATH = PROJECT_ROOT / "src" / "config" / "shows.json"
_MEMORY_PATH = PROJECT_ROOT / "src" / "config" / "memory.json"

logger = logging.getLogger(__name__)


def _read_memory_or_empty():
    try:
        return read_last_shows_from_memory()
    except FileNotFoundError:
        return {}


def write_last_shows_to_memory():
    with open(_SHOWS_PATH, encoding="utf-8") as f:
        show_album = json.load(f)

    raw_data = {}
    for name, ids in show_album.items():
        try:
            raw_data[name] = get_titles(ids["owner_id"], ids["album_id"], ids["sort"])
        except Exception as e:
            logger.error("Failed to fetch show '%s': %s", name, e)

    sorted_shows = sorted(
        [item for item in raw_data.items() if item[1]], 
        key=lambda x: x[1][0]['date'], 
        reverse=True
    )

    previous_data = _read_memory_or_empty()
    seen_by_url = {
        video["url"]: video.get("seen", False)
        for releases in previous_data.values()
        for video in releases
    }

    data_to_dump = {
        name: [
            {
                "title": v["title"], 
                "date": datetime.fromtimestamp(v["date"]).strftime("%d.%m.%Y"),
                "date_num": v["date"],
                "url": v["url"],
                "seen": seen_by_url.get(v["url"], False),
            } for v in releases
        ] for name, releases in sorted_shows
    }

    with open(_MEMORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(data_to_dump, f, ensure_ascii=False, indent=4)
    logger.info("memory.json written with %d shows", len(data_to_dump))


def read_last_shows_from_memory():
    with open(_MEMORY_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def set_video_seen(video_url, seen):
    """Persist the watched state for a video identified by its URL."""
    data = read_last_shows_from_memory()

    for releases in data.values():
        for video in releases:
            if video["url"] == video_url:
                video["seen"] = seen
                with open(_MEMORY_PATH, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                return

    raise ValueError(f"Video with URL {video_url!r} was not found in memory")
