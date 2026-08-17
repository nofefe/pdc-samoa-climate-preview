"""Embed the original botanical taro-leaf object in the Taleni draft without exposing credentials."""
import base64
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

CREDENTIALS = Path("/Users/ainsley/.hermes/family/credentials/taleni-wordpress-hermes-publisher.json")
IMAGE = Path("artifacts/taro-leaf-object.png")
FILENAME = "pacific-dataviz-taro-leaf-object.png"
MARKER = "<!-- botanical-object: taro-leaf -->"
PAGE_ID = 219


def pick(config, *names):
    for name in names:
        if config.get(name): return config[name]
    raise KeyError("missing credential configuration field")


def main():
    config = json.loads(CREDENTIALS.read_text())
    base = pick(config, "rest_base", "rest_url", "wp_rest_base", "base_url").rstrip("/")
    if not base.endswith("/wp-json/wp/v2"): base += "/wp-json/wp/v2"
    token = base64.b64encode(f"{pick(config,'username','user')}:{pick(config,'application_password','app_password','password')}".encode()).decode()

    def call(path, method="GET", body=None, content_type=None):
        headers = {"Authorization": f"Basic {token}", "Accept":"application/json"}
        if content_type: headers["Content-Type"] = content_type
        if path == "/media" and body is not None: headers["Content-Disposition"] = f'attachment; filename="{FILENAME}"'
        with urlopen(Request(base + path, data=body, headers=headers, method=method), timeout=30) as response:
            return json.loads(response.read())

    try:
        me = call("/users/me")
        page = call(f"/pages/{PAGE_ID}?context=edit")
        media_probe = call("/media?context=edit&per_page=1")
        if page.get("status") != "draft": raise RuntimeError("Refusing to alter a non-draft page")
        results = call(f"/media?context=edit&search={quote(FILENAME)}&per_page=20")
        media = next((item for item in results if item.get("slug") == FILENAME.removesuffix(".png")), None)
        if not media:
            media = call("/media", "POST", IMAGE.read_bytes(), "image/png")
            media = call(f"/media/{media['id']}", "POST", json.dumps({"title":"Pacific Dataviz — botanical taro leaf"}).encode(), "application/json")
        url = media.get("source_url")
        if not isinstance(url, str) or not url.startswith("https://"): raise RuntimeError("No usable media URL returned")
        content = page["content"]["raw"]
        if MARKER not in content:
            figure = f'''{MARKER}
<figure>
  <img src="{url}" alt="Original abstract botanical taro-leaf object" />
  <figcaption><strong>Botanical object — Draft 0.2.</strong> An original taro-leaf study for the visual direction; it is not presented as a traditional Samoan motif or cultural pattern.</figcaption>
</figure>
'''
            anchor = "<section>\n  <h2>The story question</h2>"
            if anchor not in content: raise RuntimeError("Expected draft anchor absent; refusing blind overwrite")
            call(f"/pages/{PAGE_ID}", "POST", json.dumps({"content": content.replace(anchor, figure + "\n" + anchor, 1)}).encode(), "application/json")
        after = call(f"/pages/{PAGE_ID}?context=edit")
        saved = after["content"]["raw"]
        checks = {"authenticated_user_id":me.get("id"), "media_edit_probe_items":len(media_probe), "media_id":media.get("id"), "page_id":after.get("id"), "page_status":after.get("status"), "leaf_object_embedded": MARKER in saved and url in saved}
        if checks["page_status"] != "draft" or not checks["leaf_object_embedded"]: raise RuntimeError("Draft read-back failed")
        print(json.dumps(checks, indent=2))
    except HTTPError as error:
        raise RuntimeError(f"WordPress request failed with HTTP {error.code}") from error

if __name__ == "__main__": main()
