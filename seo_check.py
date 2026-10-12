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
    need(os.path.exists(os.path.join(OUT, t["path"], "legal", "index.html")), "legal page missing")
    need(os.path.exists(os.path.join(OUT, "go", code, "index.html")), "redirect missing")
for f in ("sitemap.xml", "robots.txt", "404.html", "og.png", "favicon.svg"):
    if not os.path.exists(os.path.join(OUT, f)):
        errors.append(f"missing {f}")
if errors:
    print("SEO check FAILED:\n- " + "\n- ".join(errors)); sys.exit(1)
print(f"SEO check passed: {len(S)} pages, no issues.")
