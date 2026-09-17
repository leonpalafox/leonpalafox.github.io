"""HTTP fetching with an on-disk cache.

The cache is what makes the pipeline reproducible: every raw page is stored
under `cache/<season>-wk<week>/<source-id>.html`, so a run can be re-executed
without touching the network and a past week can be re-derived byte-for-byte.

Only the standard library is used. `timeout` is applied per request, and a
non-200 response is reported as a fetch error rather than silently cached.
"""

from __future__ import annotations

import gzip
import hashlib
import pathlib
import time
import urllib.error
import urllib.request
import zlib

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
)

RETRYABLE_STATUS = {408, 425, 429, 500, 502, 503, 504}


class FetchError(RuntimeError):
    """Raised when a page cannot be retrieved."""


def _decode(body: bytes, encoding_header: str | None) -> str:
    if encoding_header and "gzip" in encoding_header.lower():
        try:
            body = gzip.decompress(body)
        except OSError:
            pass
    elif encoding_header and "deflate" in encoding_header.lower():
        try:
            body = zlib.decompress(body, -zlib.MAX_WBITS)
        except zlib.error:
            pass
    for encoding in ("utf-8", "latin-1"):
        try:
            return body.decode(encoding)
        except UnicodeDecodeError:
            continue
    return body.decode("utf-8", errors="replace")


def cache_path(cache_dir: pathlib.Path, source_id: str) -> pathlib.Path:
    return cache_dir / f"{source_id}.html"


def fetch(
    url: str,
    source_id: str,
    cache_dir: pathlib.Path,
    *,
    max_age_seconds: int = 6 * 60 * 60,
    retries: int = 2,
    timeout: float = 25.0,
    offline: bool = False,
) -> tuple[str, str]:
    """Return (html, provenance) for `url`.

    provenance is one of "cache", "network", or "stale-cache" (network failed
    but a cached copy existed). With offline=True the network is never touched.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_path(cache_dir, source_id)

    if path.exists():
        age = time.time() - path.stat().st_mtime
        if offline or age < max_age_seconds:
            return path.read_text(encoding="utf-8"), "cache"

    if offline:
        raise FetchError(f"{source_id}: no cached copy at {path}")

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "close",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read()
                html = _decode(body, response.headers.get("Content-Encoding"))
                if response.status != 200:
                    raise FetchError(f"{source_id}: HTTP {response.status} for {url}")
                if not html.strip():
                    raise FetchError(f"{source_id}: empty body from {url}")
                path.write_text(html, encoding="utf-8")
                return html, "network"
        except urllib.error.HTTPError as exc:
            last_error = FetchError(f"{source_id}: HTTP {exc.code} for {url}")
            if exc.code not in RETRYABLE_STATUS:
                break
        except Exception as exc:  # noqa: BLE001 - network layer, report and retry
            last_error = FetchError(f"{source_id}: {type(exc).__name__}: {exc}")

        if attempt < retries:
            time.sleep(1.5 * (attempt + 1))

    if path.exists():
        return path.read_text(encoding="utf-8"), "stale-cache"
    raise last_error or FetchError(f"{source_id}: unreachable")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
