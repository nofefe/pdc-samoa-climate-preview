"""Upload individual full-width chart panels to the authorised Taleni draft media library."""
import base64
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

CREDENTIALS = Path("/Users/ainsley/.hermes/family/credentials/taleni-wordpress-hermes-publisher.json")
PANELS = [
    (Path("artifacts/chart-rainfall.png"), "pacific-dataviz-panel-rainfall.png", "Pacific Dataviz — Samoa rainfall panel"),
    (Path("artifacts/chart-sst.png"), "pacific-dataviz-panel-sst.png", "Pacific Dataviz — Samoa SST panel"),
    (Path("artifacts/chart-taro.png"), "pacific-dataviz-panel-taro.png", "Pacific Dataviz — Samoa taro panel"),
]


def pick(config, *keys):
    for key in keys:
        if isinstance(config.get(key), str) and config[key]: return config[key]
    raise KeyError("Required WordPress configuration field missing")


def main():
    config = json.loads(CREDENTIALS.read_text())
    base = pick(config, "rest_base", "rest_url", "wp_rest_base", "base_url").rstrip("/")
    if not base.endswith("/wp-json/wp/v2"): base += "/wp-json/wp/v2"
    token = base64.b64encode(f"{pick(config,'username','user')}:{pick(config,'application_password','app_password','password')}".encode()).decode()

    def request(path, method="GET", body=None, content_type=None, filename=None):
        headers = {"Authorization": f"Basic {token}", "Accept":"application/json"}
        if content_type: headers["Content-Type"] = content_type
        if filename: headers["Content-Disposition"] = f'attachment; filename="{filename}"'
        with urlopen(Request(base + path, data=body, headers=headers, method=method), timeout=45) as response:
            return json.loads(response.read())

    try:
        me = request("/users/me")
        probe = request("/media?context=edit&per_page=1")
        uploaded = []
        for path, filename, title in PANELS:
            matches = request(f"/media?context=edit&search={quote(filename)}&per_page=20")
            media = next((item for item in matches if item.get("slug") == filename.removesuffix(".png")), None)
            if not media:
                media = request("/media", "POST", path.read_bytes(), "image/png", filename)
                media = request(f"/media/{media['id']}", "POST", json.dumps({"title":title}).encode(), "application/json")
            uploaded.append({"name":filename, "id":media.get("id"), "source_url":media.get("source_url")})
    except HTTPError as error:
        raise RuntimeError(f"WordPress media request failed with HTTP {error.code}") from error
    if not all(item["id"] and isinstance(item["source_url"], str) and item["source_url"].startswith("https://") for item in uploaded):
        raise RuntimeError("One or more chart panels did not receive a usable media record")
    print(json.dumps({"authenticated_user_id":me.get("id"), "media_edit_probe_items":len(probe), "panels":uploaded}, indent=2))

if __name__ == "__main__": main()
