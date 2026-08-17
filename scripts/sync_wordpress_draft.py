"""Save the current evidence-led design outline to the authorised Taleni WordPress draft.

Credentials remain local and are never printed. This script preserves the page's
existing publication status and proves it remains a draft after write/read-back.
"""

from __future__ import annotations

import base64
import json
import re
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

CREDENTIALS = Path("/Users/ainsley/.hermes/family/credentials/taleni-wordpress-hermes-publisher.json")
PAGE_ID = 219

CONTENT = """<!-- Pacific Dataviz Challenge 2026: Draft 0.2 — not public -->
<section>
  <p><strong>DRAFT 0.2 · NOT FOR PUBLICATION</strong></p>
  <h1>The Year We Plan For</h1>
  <p><em>Samoa’s rain, heat and the decisions between them.</em></p>
  <p>This WordPress page preserves the current editorial design for the Pacific Dataviz Challenge. The working interactive is built and tested separately as a static Astro application; this page is its private CMS draft and evidence record.</p>
</section>

<section>
  <h2>The story question</h2>
  <p>How can Samoa prepare water and food systems for climate variability and long-run change while being honest about uncertainty and local-data limits?</p>
  <p><strong>Central proposition:</strong> resilience cannot be planned around an average year. Samoa-wide rainfall and Samoa EEZ sea-surface-temperature data give country-level context; they do not predict village water security, household outcomes or crop yields.</p>
</section>

<section>
  <h2>Draft story sequence</h2>
  <ol>
    <li><strong>Rainfall variability:</strong> observed annual Samoa-wide precipitation anomalies, with the 1991–2020 baseline and reported uncertainty.</li>
    <li><strong>Ocean context:</strong> observed annual Samoa EEZ sea-surface-temperature anomalies, clearly distinct from coastal or inshore measurements.</li>
    <li><strong>Start with taro:</strong> a descriptive annual Samoa taro-yield view (1961–2024, kg/ha), selected because SPC describes taro as Samoa’s most commonly grown root crop and preferred starchy staple.</li>
    <li><strong>Evidence gates:</strong> no seasonal product without documented hindcast skill; no local/catchment claims without authorised quality-controlled local data and appropriate review.</li>
  </ol>
</section>

<section>
  <h2>Why taro is the opening crop</h2>
  <p>Taro is a food-resilience anchor, not a claim that it is largest under every economic measure. It connects household food, livelihoods and trade. SPC reports it was grown by more than 18,347 households in 2015; this is historical context, not a current estimate.</p>
  <p>An FAO Samoa study documents the destructive taro-leaf-blight outbreak of 1993. The design uses this independently documented history to ask resilience questions; it does not attribute the yield series to rainfall, sea-surface temperature or a single event.</p>
</section>

<section>
  <h2>Non-negotiable evidence boundaries</h2>
  <ul>
    <li>Not a forecast or causal estimate.</li>
    <li>No village, catchment, household or water-system prediction from Samoa-wide / EEZ annual series.</li>
    <li>No crop-yield forecast or implied climate causality.</li>
    <li>Missing values remain missing; sparse disaster data are not converted to zeroes.</li>
    <li>Published seasonal outlooks and long-run scenarios must remain visually distinct from observations.</li>
  </ul>
</section>

<section>
  <h2>Sources retained in the local evidence manifest</h2>
  <ul>
    <li><a href="https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_CLIMATE_CHANGE,1.0/A.RAIN_ANOM.WS?dimensionAtObservation=AllDimensions">SPC / Pacific Data Hub Samoa rainfall anomalies</a></li>
    <li><a href="https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_CLIMATE_CHANGE,1.0/A.SST_ANOM.WS?dimensionAtObservation=AllDimensions">SPC / Pacific Data Hub Samoa EEZ SST anomalies</a></li>
    <li><a href="https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_AGRICULTURAL_PRODUCTION,1.0/A.WS.TARO.CROP_YIELD?dimensionAtObservation=AllDimensions">SPC / Pacific Data Hub Samoa taro yield</a></li>
    <li><a href="https://pafpnet.spc.int/policy-bank/countries/samoa">SPC Samoa Agriculture Policy Bank</a></li>
    <li><a href="https://www.fao.org/4/y8345e/y8345e03.htm">FAO Samoa taro-leaf-blight history</a></li>
  </ul>
</section>

<p><strong>Publication status:</strong> draft only. No public release, navigation, infrastructure or access-control change is authorised by this page update.</p>
"""


def config_value(config: dict, *keys: str) -> str:
    for key in keys:
        value = config.get(key)
        if isinstance(value, str) and value:
            return value
    raise KeyError(f"Missing one of: {', '.join(keys)}")


def main() -> None:
    config = json.loads(CREDENTIALS.read_text())
    rest_base = config_value(config, "rest_base", "rest_url", "wp_rest_base", "base_url").rstrip("/")
    if not rest_base.endswith("/wp-json/wp/v2"):
        rest_base = f"{rest_base}/wp-json/wp/v2"
    username = config_value(config, "username", "user")
    password = config_value(config, "application_password", "app_password", "password")
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    headers = {"Authorization": f"Basic {token}", "Accept": "application/json"}

    def request(path: str, method: str = "GET", body: dict | None = None) -> dict:
        request_headers = dict(headers)
        payload = None
        if body is not None:
            payload = json.dumps(body).encode()
            request_headers["Content-Type"] = "application/json"
        req = Request(f"{rest_base}{path}", data=payload, headers=request_headers, method=method)
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read())

    try:
        me = request("/users/me")
        before = request(f"/pages/{PAGE_ID}?context=edit")
        if before.get("status") != "draft":
            raise RuntimeError(f"Refusing to edit page {PAGE_ID}: current status is {before.get('status')!r}, not draft")
        request(f"/pages/{PAGE_ID}", "POST", {"content": CONTENT})
        after = request(f"/pages/{PAGE_ID}?context=edit")
    except HTTPError as error:
        raise RuntimeError(f"WordPress request failed with HTTP {error.code}") from error

    rendered = after.get("content", {}).get("raw", "")
    checks = {
        "authenticated_user_id": me.get("id"),
        "page_id": after.get("id"),
        "page_status": after.get("status"),
        "title": after.get("title", {}).get("raw"),
        "has_taro_section": "Why taro is the opening crop" in rendered,
        "has_draft_marker": "DRAFT 0.2" in rendered,
        "has_private_family_detail": bool(re.search(r"\b(faiafai|iva|savai(?:i)?|aiga house|my dad)\b", rendered, flags=re.IGNORECASE)),
    }
    if (checks["page_status"] != "draft" or not checks["has_taro_section"]
            or not checks["has_draft_marker"] or checks["has_private_family_detail"]):
        raise RuntimeError("WordPress read-back did not meet draft integrity/privacy checks")
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    main()
