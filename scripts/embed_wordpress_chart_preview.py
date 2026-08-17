"""Upload the reviewed chart snapshot and place it in the authorised Taleni draft.

The image is a static review preview of the separate Astro interactive; it does
not pretend to make the WordPress page the production interactive application.
No credentials are emitted.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

CREDENTIALS = Path("/Users/ainsley/.hermes/family/credentials/taleni-wordpress-hermes-publisher.json")
IMAGE = Path("artifacts/draft-framework.png")
PAGE_ID = 219
MEDIA_FILENAME = "pacific-dataviz-samoa-taro-draft-0-2.png"
FIGURE_MARKER = "<!-- chart-preview: pacific-dataviz-draft-0-2 -->"


def value(config: dict, *keys: str) -> str:
    for key in keys:
        candidate = config.get(key)
        if isinstance(candidate, str) and candidate:
            return candidate
    raise KeyError(f"Missing one of: {', '.join(keys)}")


def main() -> None:
    config = json.loads(CREDENTIALS.read_text())
    rest_base = value(config, "rest_base", "rest_url", "wp_rest_base", "base_url").rstrip("/")
    if not rest_base.endswith("/wp-json/wp/v2"):
        rest_base = f"{rest_base}/wp-json/wp/v2"
    auth = base64.b64encode(f"{value(config, 'username', 'user')}:{value(config, 'application_password', 'app_password', 'password')}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}", "Accept": "application/json"}

    def request(path: str, method: str = "GET", body: bytes | None = None, content_type: str | None = None) -> Any:
        request_headers = dict(headers)
        if content_type:
            request_headers["Content-Type"] = content_type
        if path == "/media" and body is not None:
            request_headers["Content-Disposition"] = f'attachment; filename="{MEDIA_FILENAME}"'
        req = Request(f"{rest_base}{path}", data=body, headers=request_headers, method=method)
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read())

    try:
        me = request("/users/me")
        media_probe = request("/media?context=edit&per_page=1")
        page = request(f"/pages/{PAGE_ID}?context=edit")
        if page.get("status") != "draft":
            raise RuntimeError("Refusing to edit a non-draft page")

        matches = request(f"/media?context=edit&search={quote(MEDIA_FILENAME)}&per_page=20")
        existing = next((item for item in matches if item.get("slug") == MEDIA_FILENAME.removesuffix(".png")), None)
        if existing:
            media = existing
        else:
            payload = IMAGE.read_bytes()
            media = request(
                "/media",
                "POST",
                payload,
                "image/png",
            )
            # Give the upload a useful title after creation; preserves binary upload simplicity.
            media = request(f"/media/{media['id']}", "POST", json.dumps({"title": "Pacific Dataviz — Samoa taro Draft 0.2 chart preview"}).encode(), "application/json")

        source_url = media.get("source_url")
        if not isinstance(source_url, str) or not source_url.startswith("https://"):
            raise RuntimeError("Media upload returned no usable HTTPS source URL")
        content = page.get("content", {}).get("raw", "")
        figure = f'''{FIGURE_MARKER}
<figure>
  <img src="{source_url}" alt="Draft chart preview: Samoa rainfall anomalies, Samoa EEZ sea-surface-temperature anomalies, and annual taro yield" />
  <figcaption><strong>Chart preview — Draft 0.2.</strong> This is a static review image of the separate interactive draft. It includes the observed annual Samoa-wide rainfall, Samoa EEZ SST and Samoa taro-yield views; it is not a forecast or causal estimate.</figcaption>
</figure>
'''
        if FIGURE_MARKER not in content:
            anchor = "<section>\n  <h2>Sources retained in the local evidence manifest</h2>"
            if anchor not in content:
                raise RuntimeError("Draft content anchor not found; refusing a blind overwrite")
            content = content.replace(anchor, figure + "\n" + anchor, 1)
            request(f"/pages/{PAGE_ID}", "POST", json.dumps({"content": content}).encode(), "application/json")

        after = request(f"/pages/{PAGE_ID}?context=edit")
        rendered = after.get("content", {}).get("raw", "")
        checks = {
            "authenticated_user_id": me.get("id"),
            "media_edit_probe_items": len(media_probe),
            "media_id": media.get("id"),
            "page_id": after.get("id"),
            "page_status": after.get("status"),
            "chart_preview_embedded": FIGURE_MARKER in rendered and source_url in rendered,
        }
        if checks["page_status"] != "draft" or not checks["chart_preview_embedded"]:
            raise RuntimeError("WordPress chart-preview read-back failed")
        print(json.dumps(checks, indent=2))
    except HTTPError as error:
        raise RuntimeError(f"WordPress request failed with HTTP {error.code}") from error


if __name__ == "__main__":
    main()
