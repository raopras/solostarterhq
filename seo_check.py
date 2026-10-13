"""Publish-time SEO checks. Exits non-zero (blocking the deploy) if any page fails."""
import html, json, os, re, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "dist"
S = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "strings.json"), encoding="utf-8"))
errors = []
titles = set()
for code, t in S.items():
    f = os.path.join(OUT, t["path"], "index.html")
    if not os.path.exists(f):
        errors.append(f"{code}: page missing"); continue
    s = open(f, encoding="utf-8").read()
    def need(cond, msg):
        if not cond: errors.append(f"{code}: {msg}")
    title = html.unescape(re.search(r"<title>(.*?)</title>", s).group(1))
    desc = html.unescape(re.search(r'name="description" content="(.*?)"', s).group(1))
    need(len(title) <= 60, f"title too long ({len(title)})")
    need(title not in titles, "duplicate title"); titles.add(title)
    need(70 <= len(desc) <= 160, f"description length {len(desc)}")
    need(s.count("<h1") == 1, "needs exactly one H1")
    need('rel="canonical"' in s, "missing canonical")
    need(s.count('rel="alternate" hreflang=') == len(S) + 1, "hreflang set incomplete")
    need(f'<html lang="{t["htmllang"]}"' in s, "wrong html lang")
    need('og:image' in s and 'og:title' in s, "missing social tags")
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(block)
        except Exception: errors.append(f"{code}: invalid JSON-LD")
    need('rel="sponsored nofollow noopener"' in s, "affiliate links missing rel=sponsored")
    for slug in ("legal", "privacy", "how-we-make-money"):
        need(os.path.exists(os.path.join(OUT, t["path"], slug, "index.html")), f"{slug} page missing")
    need('class="adbar"' in s, "ad label missing at top of page")
    need(os.path.exists(os.path.join(OUT, "go", code, "index.html")), "redirect missing")
# Guide pages: same SEO rules, plus affiliate-compliance rules.
G = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "guides.json"), encoding="utf-8"))
# systeme.io's affiliate agreement: "you may not use any other competitor trademarks in your promotion".
COMPETITORS = ["ClickFunnels", "Leadpages", "Mailchimp", "ConvertKit", "Kajabi", "Kartra", "Teachable", "Thinkific", "Podia",
               "Wix", "Squarespace", "WordPress", "Calendly", "Acuity", "Tapfiliate", "Zapier", "ActiveCampaign", "Keap",
               "Shopify", "Gumroad", "Samcart", "ThriveCart", "Substack", "Beehiiv", "GetResponse", "Systeme.io"]
for code, gl in G.items():
    files = [("hub", os.path.join(OUT, S[code]["path"], gl["dir"], "index.html"))]
    files += [(p["slug"], os.path.join(OUT, S[code]["path"], gl["dir"], p["slug"], "index.html")) for p in gl["pages"]]
    for name, f in files:
        tag = f"{code} guide {name}"
        if not os.path.exists(f):
            errors.append(f"{tag}: page missing"); continue
        s = open(f, encoding="utf-8").read()
        def need(cond, msg):
            if not cond: errors.append(f"{tag}: {msg}")
        title = html.unescape(re.search(r"<title>(.*?)</title>", s).group(1))
        desc = html.unescape(re.search(r'name="description" content="(.*?)"', s).group(1))
        need(len(title) <= 60, f"title too long ({len(title)})")
        need(title not in titles, "duplicate title"); titles.add(title)
        need(70 <= len(desc) <= 160, f"description length {len(desc)}")
        need(s.count("<h1") == 1, "needs exactly one H1")
        need('rel="canonical"' in s, "missing canonical")
        need(f'<html lang="{S[code]["htmllang"]}"' in s, "wrong html lang")
        need('og:image' in s and 'og:title' in s, "missing social tags")
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try: json.loads(block)
            except Exception: errors.append(f"{tag}: invalid JSON-LD")
        need('class="adbar"' in s, "ad label missing at top of page")
        buttons = re.findall(r'<a class="btn[^"]*" href="/go/' + re.escape(code) + r'/" rel="sponsored nofollow noopener"', s)
        need(len(buttons) >= 4, f"only {len(buttons)} sign-up buttons")
        need(S[code]["disclosure"].split(":")[0] in html.unescape(s), "affiliate disclosure missing")
        need(html.unescape(s).count(S[code]["cta_note"]) >= 2, "Ad note missing next to the buttons")
        need('id="copy-url"' in s, "copy-link box missing")
        for c in COMPETITORS:
            if re.search(r"\b" + re.escape(c) + r"\b", html.unescape(re.sub(r"<script.*?</script>", "", s, flags=re.S))):
                errors.append(f"{tag}: names a competitor or misspells the brand ({c})")
for f in ("sitemap.xml", "robots.txt", "404.html", "og.png", "favicon.svg"):
    if not os.path.exists(os.path.join(OUT, f)):
        errors.append(f"missing {f}")
if errors:
    print("SEO check FAILED:\n- " + "\n- ".join(errors)); sys.exit(1)
print(f"SEO check passed: {len(S)} landing pages and {sum(len(g['pages']) + 1 for g in G.values())} guide pages, no issues.")
