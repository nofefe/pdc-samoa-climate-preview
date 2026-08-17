"""Assign Taleni's verified blank page shell to page 219 and read it back."""
import base64
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

CREDENTIALS = Path("/Users/ainsley/.hermes/family/credentials/taleni-wordpress-hermes-publisher.json")
PAGE_ID = 219
TEMPLATE = "taleni-page-shell"


def pick(config, *keys):
    for key in keys:
        if isinstance(config.get(key), str) and config[key]: return config[key]
    raise KeyError("Required WordPress configuration field missing")


def main():
    config = json.loads(CREDENTIALS.read_text())
    base = pick(config, "rest_base", "rest_url", "wp_rest_base", "base_url").rstrip("/")
    if not base.endswith("/wp-json/wp/v2"): base += "/wp-json/wp/v2"
    token = base64.b64encode(f"{pick(config, 'username', 'user')}:{pick(config, 'application_password', 'app_password', 'password')}".encode()).decode()

    def request(path, method="GET", body=None):
        headers = {"Authorization": f"Basic {token}", "Accept":"application/json"}
        data = None
        if body is not None:
            data = json.dumps(body).encode(); headers["Content-Type"] = "application/json"
        with urlopen(Request(base + path, data=data, headers=headers, method=method), timeout=30) as response:
            return json.loads(response.read())

    try:
        me = request("/users/me")
        before = request(f"/pages/{PAGE_ID}?context=edit")
        if before.get("status") != "draft": raise RuntimeError("Refusing to change a non-draft page")
        request(f"/pages/{PAGE_ID}", "POST", {"template": TEMPLATE})
        after = request(f"/pages/{PAGE_ID}?context=edit")
    except HTTPError as error:
        raise RuntimeError(f"WordPress request failed with HTTP {error.code}") from error

    checks = {"authenticated_user_id":me.get("id"), "page_id":after.get("id"), "page_status":after.get("status"), "template":after.get("template"), "content_preserved": "pdc-story" in after.get("content", {}).get("raw", "")}
    if checks["page_status"] != "draft" or checks["template"] != TEMPLATE or not checks["content_preserved"]: raise RuntimeError("Blank-template read-back failed")
    print(json.dumps(checks, indent=2))

if __name__ == "__main__": main()
