import os


def _set_or_none(name: str) -> set[str] | None:
    env = os.getenv(name)
    if not env:
        return None

    return set(v.strip() for v in env.split(",") if v.strip())


HOST = os.getenv("DLHDHR_HOST", "127.0.0.1")
PORT: int = int(os.getenv("DLHDHR_PORT", 8000))
DEBUG: bool = os.getenv("DLHDHR_DEBUG", "0").lower() in ("1", "true")

DLHD_BASE_URL = os.getenv("DLHD_BASE_URL", "https://dlhd.sx/")
DLHD_INDEX_M3U8_PATTERN = os.getenv(
    "DLHD_INDEX_M3U8_PATTERN", "https://webudit.webhd.ru/lb/premium{channel.number}/index.m3u8"
)

CHANNEL_EXCLUDE: set[str] | None = _set_or_none("DLHDHR_CHANNEL_EXCLUDE")
CHANNEL_ALLOW: set[str] | None = _set_or_none("DLHDHR_CHANNEL_ALLOW")
COUNTRY_EXCLUDE: set[str] | None = _set_or_none("DLHDHR_COUNTRY_EXCLUDE")
COUNTRY_ALLOW: set[str] | None = _set_or_none("DLHDHR_COUNTRY_ALLOW")

ZAP2IT_REFRESH_DELAY: int = int(os.getenv("DLHDHR_ZAP2IT_REFRESH_DELAY", "3600"))
