"""Replace Taleni page 219's plain draft outline with a scoped editorial design.

The page remains a private draft. It intentionally uses a static chart preview:
the production interactive continues to be a separately built Astro application.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

CREDENTIALS = Path("/Users/ainsley/.hermes/family/credentials/taleni-wordpress-hermes-publisher.json")
PAGE_ID = 219


def get_value(config: dict, *keys: str) -> str:
    for key in keys:
        candidate = config.get(key)
        if isinstance(candidate, str) and candidate:
            return candidate
    raise KeyError("Required WordPress configuration field is missing")


def main() -> None:
    config = json.loads(CREDENTIALS.read_text())
    base = get_value(config, "rest_base", "rest_url", "wp_rest_base", "base_url").rstrip("/")
    if not base.endswith("/wp-json/wp/v2"):
        base = f"{base}/wp-json/wp/v2"
    credentials = base64.b64encode(f"{get_value(config, 'username', 'user')}:{get_value(config, 'application_password', 'app_password', 'password')}".encode()).decode()

    def request(path: str, method: str = "GET", body: dict | None = None) -> dict:
        headers = {"Authorization": f"Basic {credentials}", "Accept": "application/json"}
        payload = None
        if body is not None:
            payload = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
        with urlopen(Request(base + path, data=payload, headers=headers, method=method), timeout=30) as response:
            return json.loads(response.read())

    try:
        me = request("/users/me")
        page = request(f"/pages/{PAGE_ID}?context=edit")
        leaf = request("/media/226?context=edit")
        charts = request("/media/224?context=edit")
        if page.get("status") != "draft":
            raise RuntimeError("Refusing to redesign a page that is not a draft")
        leaf_url, chart_url = leaf.get("source_url"), charts.get("source_url")
        if not all(isinstance(url, str) and url.startswith("https://") for url in (leaf_url, chart_url)):
            raise RuntimeError("Expected WordPress media URLs were not available")

        content = f'''<!-- Pacific Dataviz Challenge 2026 · Editorial Draft 0.2 · not public -->
<div class="pdc-story">
<style>
.pdc-story{{--ink:#163b3b;--cream:#f4efe4;--leaf:#3e7657;--sun:#d29d55;--mist:#dce8df;--line:rgba(22,59,59,.2);color:var(--ink);font-family:Georgia,serif;line-height:1.6;background:var(--cream);margin:0 auto;max-width:1120px;overflow:hidden}}.pdc-story *{{box-sizing:border-box}}.pdc-story .pdc-hero{{position:relative;min-height:570px;padding:74px clamp(26px,7vw,88px);display:grid;align-content:center;background:radial-gradient(circle at 82% 22%,#d7e6c0 0,transparent 31%),linear-gradient(135deg,#e8efe2 0%,#f4efe4 68%)}}.pdc-story .pdc-kicker{{font:700 11px/1.3 ui-monospace,monospace;letter-spacing:.13em;color:#326d68;margin:0 0 18px}}.pdc-story h1,.pdc-story h2,.pdc-story h3{{color:var(--ink);line-height:1.02;margin:0;text-wrap:balance}}.pdc-story h1{{font-size:clamp(54px,9vw,104px);max-width:690px}}.pdc-story h2{{font-size:clamp(35px,5vw,58px)}}.pdc-story h3{{font-size:24px}}.pdc-story .pdc-standfirst{{font-size:clamp(22px,3vw,34px);max-width:620px;margin:22px 0 0}}.pdc-story .pdc-dek{{max-width:625px;font-family:Arial,sans-serif;color:#45615d;margin:20px 0 0;font-size:16px}}.pdc-story .pdc-leaf{{position:absolute;right:-22px;bottom:-37px;width:min(46vw,430px);opacity:.95;pointer-events:none}}.pdc-story .pdc-section{{padding:72px clamp(26px,7vw,88px);border-top:1px solid var(--line)}}.pdc-story .pdc-label{{font:700 11px/1.3 ui-monospace,monospace;letter-spacing:.12em;color:#326d68;margin:0 0 14px}}.pdc-story .pdc-copy{{max-width:720px;font-family:Arial,sans-serif;color:#45615d;font-size:17px}}.pdc-story .pdc-copy strong{{color:var(--ink)}}.pdc-story .pdc-question{{background:#f9f6ee}}.pdc-story .pdc-chart{{margin:30px 0 0;background:#fffdf8;padding:11px;border:1px solid rgba(0,0,0,.1);box-shadow:0 20px 45px rgba(18,55,50,.12)}}.pdc-story .pdc-chart img{{display:block;width:100%;height:auto;outline:1px solid rgba(0,0,0,.1)}}.pdc-story figcaption{{font:14px/1.5 Arial,sans-serif;color:#506761;padding:13px 8px 4px}}.pdc-story .pdc-taro{{background:var(--leaf);color:#eff5e8;display:grid;grid-template-columns:1fr 1fr;gap:44px;align-items:start}}.pdc-story .pdc-taro h2,.pdc-story .pdc-taro h3{{color:#fff9e9}}.pdc-story .pdc-taro .pdc-label,.pdc-story .pdc-taro .pdc-copy{{color:#dcebd1}}.pdc-story .pdc-cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:32px}}.pdc-story .pdc-card{{padding:24px 22px;background:#e4ede0;border-top:4px solid var(--sun);font-family:Arial,sans-serif;color:#45615d}}.pdc-story .pdc-card h3{{font-family:Georgia,serif;margin-bottom:10px}}.pdc-story .pdc-card p{{margin:0}}.pdc-story .pdc-gate{{background:#183e3d;color:#edf0df}}.pdc-story .pdc-gate h2{{color:#fff9e9}}.pdc-story .pdc-gate ul{{margin:25px 0 0;padding-left:20px;font-family:Arial,sans-serif;max-width:760px}}.pdc-story .pdc-gate li{{margin:11px 0}}.pdc-story .pdc-sources{{font:14px/1.6 Arial,sans-serif;color:#45615d}}.pdc-story .pdc-sources a{{color:#176c70}}@media(max-width:680px){{.pdc-story .pdc-hero{{min-height:500px;padding-top:58px}}.pdc-story .pdc-leaf{{width:270px;opacity:.27;right:-70px}}.pdc-story .pdc-taro,.pdc-story .pdc-cards{{grid-template-columns:1fr}}.pdc-story .pdc-section{{padding-top:52px;padding-bottom:52px}}}}
</style>
<section class="pdc-hero">
  <div><p class="pdc-kicker">PACIFIC DATAVIZ CHALLENGE 2026 · EDITORIAL DRAFT 0.2</p><h1>The Year We Plan For</h1><p class="pdc-standfirst">Samoa’s rain, heat and the decisions between them.</p><p class="pdc-dek">A guided climate-resilience story about planning for variability — without pretending Samoa-wide and EEZ annual data can predict a village water system, household outcome or crop harvest.</p></div>
  <img class="pdc-leaf" src="{leaf_url}" alt="" aria-hidden="true" />
</section>
<section class="pdc-section pdc-question"><p class="pdc-label">THE QUESTION</p><h2>What changes when a plan meets the years Samoa has already experienced?</h2><p class="pdc-copy">Country-level rainfall and Samoa EEZ sea-surface-temperature data can provide context. They cannot decide what an individual village, catchment or household needs. Local evidence, quality metadata and appropriate review remain essential.</p></section>
<section class="pdc-section"><p class="pdc-label">01–03 · OBSERVED CONTEXT</p><h2>Average is not the year people plan for.</h2><p class="pdc-copy">The chart preview holds three separate annual views: Samoa-wide rainfall anomalies, Samoa EEZ SST anomalies, and Samoa taro yield. Their proximity is for context, <strong>not</strong> proof of causation.</p><figure class="pdc-chart"><img src="{chart_url}" alt="Draft chart preview showing Samoa rainfall anomalies, Samoa EEZ sea-surface-temperature anomalies and annual taro yield" /><figcaption><strong>Draft 0.2 chart preview.</strong> Observed annual context only — not a forecast or causal estimate.</figcaption></figure></section>
<section class="pdc-section pdc-taro"><div><p class="pdc-label">START WITH TARO</p><h2>A crop is food, livelihood, memory and resilience.</h2></div><div><h3>Why taro?</h3><p class="pdc-copy">SPC describes taro as Samoa’s most commonly grown root crop and preferred starchy staple. The yield view is descriptive: it does not claim that rainfall or temperature caused a particular year’s outcome.</p><p class="pdc-copy">The documented 1993 taro-leaf-blight shock is a reason to ask better resilience questions — not a licence to infer a cause from the plotted annual series.</p></div></section>
<section class="pdc-section"><p class="pdc-label">NEXT EVIDENCE GATE</p><h2>Design the seasonal view around variation, not false precision.</h2><div class="pdc-cards"><article class="pdc-card"><h3>Monthly rainfall</h3><p>A leaf-vein seasonal calendar could use monthly box-and-whisker distributions once a quality-controlled monthly series is verified.</p></article><article class="pdc-card"><h3>Seasonal outlook</h3><p>Show below/near/above-normal probabilities only with an authoritative product and documented hindcast skill.</p></article><article class="pdc-card"><h3>Local decisions</h3><p>Do not add village or catchment claims without authorised local data, quality metadata and context review.</p></article></div></section>
<section class="pdc-section pdc-gate"><p class="pdc-label">WHAT THIS DRAFT DOES NOT DO</p><h2>Clear boundaries are part of the design.</h2><ul><li>Forecast water-system failure, disaster impacts or crop yields.</li><li>Rank villages, communities or households.</li><li>Turn sparse or missing records into zeroes.</li><li>Use one number to define resilience.</li></ul></section>
<section class="pdc-section pdc-sources"><p class="pdc-label">SOURCES &amp; STATUS</p><p><strong>Draft only — not for public release.</strong> Source and limitation record: <a href="https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_CLIMATE_CHANGE,1.0/A.RAIN_ANOM.WS?dimensionAtObservation=AllDimensions">SPC rainfall SDMX</a> · <a href="https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_CLIMATE_CHANGE,1.0/A.SST_ANOM.WS?dimensionAtObservation=AllDimensions">SPC SST SDMX</a> · <a href="https://stats-sdmx-disseminate.pacificdata.org/rest/data/SPC,DF_AGRICULTURAL_PRODUCTION,1.0/A.WS.TARO.CROP_YIELD?dimensionAtObservation=AllDimensions">SPC taro-yield SDMX</a> · <a href="https://pafpnet.spc.int/policy-bank/countries/samoa">SPC Samoa Agriculture Policy Bank</a> · <a href="https://www.fao.org/4/y8345e/y8345e03.htm">FAO taro-leaf-blight history</a>.</p></section>
</div>'''
        request(f"/pages/{PAGE_ID}", "POST", {"content": content})
        after = request(f"/pages/{PAGE_ID}?context=edit")
    except HTTPError as error:
        raise RuntimeError(f"WordPress request failed with HTTP {error.code}") from error

    saved = after.get("content", {}).get("raw", "")
    checks = {"authenticated_user_id": me.get("id"), "page_id": after.get("id"), "page_status": after.get("status"), "editorial_shell_present": "pdc-story" in saved, "leaf_present": leaf_url in saved, "charts_present": chart_url in saved, "taro_section_present": "START WITH TARO" in saved}
    if checks["page_status"] != "draft" or not all(checks[key] for key in ("editorial_shell_present", "leaf_present", "charts_present", "taro_section_present")):
        raise RuntimeError("WordPress design read-back did not pass")
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    main()
