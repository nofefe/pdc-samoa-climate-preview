"""Inspect authorised WordPress page-template options without revealing credentials."""
import base64
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

CREDENTIALS = Path("/Users/ainsley/.hermes/family/credentials/taleni-wordpress-hermes-publisher.json")
PAGE_ID = 219


def pick(config, *keys):
    for key in keys:
        if isinstance(config.get(key), str) and config[key]:
            return config[key]
    raise KeyError("Required WordPress configuration field missing")


def main():
    config = json.loads(CREDENTIALS.read_text())
    base = pick(config, "rest_base", "rest_url", "wp_rest_base", "base_url").rstrip("/")
    if not base.endswith("/wp-json/wp/v2"):
        base += "/wp-json/wp/v2"
    auth = base64.b64encode(f"{pick(config, 'username', 'user')}:{pick(config, 'application_password', 'app_password', 'password')}".encode()).decode()

    def get(path):
        req = Request(base + path, headers={"Authorization": f"Basic {auth}", "Accept": "application/json"})
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read())

    try:
        me = get("/users/me")
        page = get(f"/pages/{PAGE_ID}?context=edit")
        response = {"authenticated_user_id": me.get("id"), "page_id": page.get("id"), "page_status": page.get("status"), "current_template": page.get("template"), "page_has_template_field": "template" in page}
        try:
            templates = get("/templates?context=edit&per_page=100")
            response["templates_endpoint"] = "available"
            response["templates"] = [{"id": item.get("id"), "slug": item.get("slug"), "title": item.get("title", {}).get("raw")} for item in templates]
            shell = next((item for item in templates if item.get("slug") == "taleni-page-shell"), None)
            if shell:
                raw = shell.get("content", {}).get("raw", "")
                lowered = raw.lower()
                response["taleni_page_shell"] = {"content_length": len(raw), "has_template_part": "wp:template-part" in lowered, "has_query_loop": "wp:query" in lowered, "has_latest_posts": "wp:latest-posts" in lowered, "has_post_content": "wp:post-content" in lowered}
        except HTTPError as error:
            response["templates_endpoint"] = f"HTTP {error.code}"
            response["templates"] = []
        print(json.dumps(response, indent=2))
    except HTTPError as error:
        raise RuntimeError(f"WordPress read failed with HTTP {error.code}") from error

if __name__ == "__main__":
    main()
