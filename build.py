"""Build the SoloStarter HQ static site from strings.json.

One template, every language. To add a language, add a block to
strings.json and rebuild. To change domain, edit BASE.
"""
import json, html, os, shutil, sys

BASE = os.environ.get("SITE_BASE", "https://solostarterhq.com").rstrip("/")
from urllib.parse import urlparse
PREFIX = urlparse(BASE).path.rstrip("/")  # e.g. "/solostarterhq" on a GitHub project site
AFF_ID = "sa0283620426244c2d54b43911545c547546a995b6"
# Each language sends visitors to systeme.io's sign-up page in the same language.
# systeme.io credits the affiliate ID on any of its pages (?sa=...).
SYSTEME_LANG = {"en": "", "es": "es/", "pt-br": "pt/", "de": "de/"}


def aff(code):
    return f"https://systeme.io/{SYSTEME_LANG[code]}register?sa={AFF_ID}"


def direct(code):
    return f"https://systeme.io/{SYSTEME_LANG[code]}"
OUT = sys.argv[1] if len(sys.argv) > 1 else "dist"
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "strings.json"), encoding="utf-8"))
LANGS = list(S.keys())
# Calculator currencies. Example amounts are set in US dollars and scaled with rough,
# rounded rates; they are labelled as examples on the page, so exactness doesn't matter.
EXAMPLES_USD = [16, 29, 49, 39, 12]
FX = {  # code: (approx units per 1 USD, rounding step)
    "USD": (1, 1), "GBP": (0.75, 1), "EUR": (0.86, 1), "CHF": (0.8, 1), "CAD": (1.38, 1), "AUD": (1.52, 1),
    "BRL": (5.4, 5), "MXN": (18.5, 10), "COP": (4000, 1000), "CLP": (950, 500), "PEN": (3.7, 1), "INR": (88, 50),
}
CURRENCIES = list(FX)
# Visitor region (from the browser's language setting) -> currency
REGION_CURRENCY = {"GB": "GBP", "US": "USD", "CA": "CAD", "AU": "AUD", "IN": "INR", "BR": "BRL", "MX": "MXN",
                   "CO": "COP", "CL": "CLP", "PE": "PEN", "CH": "CHF", "LI": "CHF",
                   **{r: "EUR" for r in "IE ES DE AT FR IT PT NL BE LU FI GR SK SI EE LV LT MT CY HR".split()}}


def examples(cur):
    rate, step = FX[cur]
    return [max(step, round(v * rate / step) * step) for v in EXAMPLES_USD]

e = html.escape


def url(code):
    return f"{BASE}/{S[code]['path']}"


CSS_BASE = """
/* Layout: one centred column; the calculator is styled as a freelancer's invoice whose total is struck out to zero. */
:root{
  --paper:#f5f7fb; --card:#ffffff; --ink:#141b2d; --muted:#566079; --line:#d9deea;
  --accent:#1d6b4a; --accent-ink:#ffffff; --marker:#ffd84a; --marker-ink:#141b2d;
  --display:"Bricolage Grotesque", "Avenir Next", "Segoe UI", system-ui, sans-serif;
  --body:"Atkinson Hyperlegible", "Segoe UI", system-ui, sans-serif;
  --mono:"JetBrains Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --paper:#0f1420; --card:#171e2e; --ink:#e8ecf5; --muted:#a3adc4; --line:#2b3448;
  --accent:#4cc38a; --accent-ink:#0b1410; --marker:#e9c53a; --marker-ink:#141b2d; color-scheme:dark}}
:root[data-theme="dark"]{
  --paper:#0f1420; --card:#171e2e; --ink:#e8ecf5; --muted:#a3adc4; --line:#2b3448;
  --accent:#4cc38a; --accent-ink:#0b1410; --marker:#e9c53a; --marker-ink:#141b2d; color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.6 var(--body)}
.wrap{max-width:68rem;margin:0 auto;padding-inline:clamp(16px,4vw,40px)}
header.top{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;padding-block:20px}
.brand{font:700 1.2rem/1 var(--display);color:var(--ink);text-decoration:none;letter-spacing:-.01em}
.brand span{color:var(--accent)}
.top nav{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.langs{display:flex;gap:4px;font:500 .8rem/1 var(--mono);text-transform:uppercase}
.langs a{color:var(--muted);text-decoration:none;padding:6px 7px;border-radius:6px}
.langs a[aria-current]{color:var(--ink);background:var(--line)}
.btn{display:inline-block;background:var(--accent);color:var(--accent-ink);font:700 1rem/1 var(--body);padding:15px 22px;border-radius:10px;text-decoration:none}
.btn.small{padding:10px 14px;font-size:.9rem}
.btn:hover{filter:brightness(1.08)}
a:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid var(--marker);outline-offset:2px}
.hero{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:clamp(24px,5vw,64px);align-items:center;padding-block:clamp(24px,6vw,72px)}
h1,h2,h3{font-family:var(--display);text-wrap:balance;letter-spacing:-.02em;margin:0}
h1{font-size:clamp(2.2rem,5.2vw,3.7rem);line-height:1.05;font-weight:800}
h2{font-size:clamp(1.6rem,3.2vw,2.3rem);line-height:1.15;font-weight:700}
h3{font-size:1.1rem}
mark{background:var(--marker);color:var(--marker-ink);padding:0 .12em;border-radius:4px}
.lede{font-size:1.15rem;color:var(--muted);max-width:36em;margin:18px 0 26px}
.adbar{margin:0;padding:8px 16px;background:var(--ink);color:var(--paper);font-size:.85rem;text-align:center}
.adbar a{color:var(--marker)}
.aud{font-weight:700;margin:-12px 0 24px;max-width:36em}
.note{font-size:.85rem;color:var(--muted);margin-top:12px;max-width:38em}
/* invoice */
.invoice{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px 22px 18px;font-family:var(--mono);box-shadow:0 18px 40px -28px rgba(20,27,45,.45)}
.inv-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap;border-bottom:2px dashed var(--line);padding-bottom:12px;margin-bottom:6px}
.inv-head b{letter-spacing:.18em;font-size:.85rem}
.inv-head label{font-size:.75rem;color:var(--muted);display:flex;gap:6px;align-items:center}
select,input{font:inherit;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:6px 8px}
.row{display:grid;grid-template-columns:minmax(0,1fr) 7.5rem;gap:10px;align-items:center;padding:7px 0;border-bottom:1px solid var(--line);font-size:.88rem}
.row label{min-width:0}
.row input{width:100%;text-align:right;font-variant-numeric:tabular-nums}
.sum{display:flex;justify-content:space-between;gap:10px;padding:8px 0;font-size:.9rem;font-variant-numeric:tabular-nums}
.sum.year s{color:var(--muted)}
.sum.free{font-weight:700;border-top:2px solid var(--ink);padding-top:10px}
.keep{margin-top:12px;background:var(--marker);color:var(--marker-ink);border-radius:8px;padding:10px 12px;font:700 1rem/1.3 var(--body)}
.ex{font-size:.72rem;color:var(--muted);margin:8px 0 0}
.ex.intro{font-family:var(--body);font-size:.82rem;margin:4px 0 6px}
section{padding-block:clamp(36px,6vw,72px)}
section+section{border-top:1px solid var(--line)}
.sec-intro{color:var(--muted);max-width:40em;margin:12px 0 0}
.facts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:12px;overflow:hidden;margin-top:28px}
.fact{background:var(--card);padding:18px 16px}
.fact dt{font-size:.8rem;color:var(--muted)}
.fact dd{margin:4px 0 0;font:700 1.35rem/1.2 var(--display)}
.steps{list-style:none;padding:0;margin:28px 0 0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;counter-reset:s}
.steps li{counter-increment:s}
.steps li::before{content:counter(s);display:inline-grid;place-items:center;width:2rem;height:2rem;border-radius:50%;background:var(--ink);color:var(--paper);font:700 .95rem/1 var(--mono);margin-bottom:12px}
.steps p{color:var(--muted);margin:6px 0 0}
.faq{margin-top:24px;max-width:46rem}
details{border-bottom:1px solid var(--line);padding:14px 0}
summary{cursor:pointer;font:700 1.05rem/1.4 var(--body)}
details p{color:var(--muted);margin:10px 0 0}
.close{text-align:left}
.close p{color:var(--muted);margin:10px 0 22px}
footer{border-top:1px solid var(--line);padding-block:28px 40px;font-size:.82rem;color:var(--muted)}
footer a{color:inherit}
footer p{max-width:60em;margin:0 0 8px}
@media (max-width:820px){.hero{grid-template-columns:1fr}.facts{grid-template-columns:repeat(2,minmax(0,1fr))}.steps{grid-template-columns:1fr}}
@media (prefers-reduced-motion:no-preference){.keep{transition:transform .2s}.keep.bump{transform:scale(1.03)}}
"""

def _face(fam, file, w):
    return f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;src:url(/fonts/{file}) format('woff2')}}"
# Fonts are served from this site (no Google Fonts), so no visitor data goes to a third party.
FONT_CSS = "".join([
    _face("Atkinson Hyperlegible", "atkinson-hyperlegible-latin-400-normal.woff2", 400),
    _face("Atkinson Hyperlegible", "atkinson-hyperlegible-latin-700-normal.woff2", 700),
    _face("Bricolage Grotesque", "bricolage-grotesque-latin-700-normal.woff2", 700),
    _face("Bricolage Grotesque", "bricolage-grotesque-latin-800-normal.woff2", 800),
    _face("JetBrains Mono", "jetbrains-mono-latin-400-normal.woff2", 400),
    _face("JetBrains Mono", "jetbrains-mono-latin-500-normal.woff2", 500),
    _face("JetBrains Mono", "jetbrains-mono-latin-700-normal.woff2", 700),
])
CSS = FONT_CSS + CSS_BASE
FONTS = '<link rel="preload" href="/fonts/bricolage-grotesque-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>'


UMAMI = os.environ.get("UMAMI_WEBSITE_ID", "").strip()


def ev(code, button):
    """Umami click event on a sign-up button (no-op when analytics is off)."""
    return f'data-umami-event="signup-click" data-umami-event-lang="{code}" data-umami-event-button="{button}"' if UMAMI else ""


def analytics():
    # Cookie-free Umami. Skipped for visitors who send Do Not Track.
    return (f'<script defer src="https://cloud.umami.is/script.js" data-website-id="{UMAMI}" '
            f'data-do-not-track="true" data-domains="solostarterhq.com"></script>') if UMAMI else ""


def head(code, preview=False):
    t = S[code]
    alts = "".join(f'<link rel="alternate" hreflang="{S[c]["hreflang"]}" href="{url(c)}">' for c in LANGS)
    alts += f'<link rel="alternate" hreflang="x-default" href="{url("en")}">'
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": t["htmllang"],
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]}
    site_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": "SoloStarter HQ", "url": BASE + "/", "inLanguage": t["htmllang"]}
    og_alts = "".join(f'<meta property="og:locale:alternate" content="{S[c]["og_locale"]}">' for c in LANGS if c != code)
    return f"""<title>{e(t['title'])}</title>
<meta name="description" content="{e(t['desc'])}">
<link rel="canonical" href="{url(code)}">{alts}
<meta property="og:type" content="website"><meta property="og:site_name" content="SoloStarter HQ">
<meta property="og:title" content="{e(t['title'])}"><meta property="og:description" content="{e(t['desc'])}">
<meta property="og:url" content="{url(code)}"><meta property="og:image" content="{BASE}/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{t['og_locale']}">{og_alts}
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1d6b4a">
<link rel="icon" href="{'' if preview else '/'}favicon.svg" type="image/svg+xml">
{FONTS}
{'' if preview else analytics()}
<script type="application/ld+json">{json.dumps(site_ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
<style>{CSS}</style>"""


def body(code, preview=False):
    t = S[code]
    root = "#" if preview else "/"
    go = aff(code) if preview else f"/go/{code}/"
    rel = 'rel="sponsored nofollow noopener"'
    cur_attr = ' aria-current="page"'
    langs = "".join(
        f'<a href="{"#" if preview else "/" + S[c]["path"]}" hreflang="{S[c]["hreflang"]}" lang="{S[c]["htmllang"]}" title="{e(S[c]["lang_name"])}"{cur_attr if c == code else ""}>{"pt" if c == "pt-br" else c}</a>'
        for c in LANGS)
    rows = "".join(
        f'<div class="row"><label for="c{i}">{e(name)}</label><input id="c{i}" type="number" inputmode="decimal" min="0" step="1" value="{v}" aria-describedby="exnote"></div>'
        for i, (name, v) in enumerate(zip(t["items"], examples(t["currency"]))))
    opts = "".join(f'<option{" selected" if c == t["currency"] else ""}>{c}</option>' for c in CURRENCIES)
    facts = "".join(f'<div class="fact"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in t["plan_items"])
    steps = "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in t["steps"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in t["faq"])
    keep_tpl = json.dumps(t["keep_line"], ensure_ascii=False)
    return f"""{banner(code, preview)}<div class="wrap">
<header class="top">
  <a class="brand" href="{root}{'' if preview else t['path']}">SoloStarter<span>HQ</span></a>
  <nav aria-label="{e(t['lang_label'])}">{'' if preview or code not in G else f'<a href="{gpath(code)}" style="color:var(--ink);font-weight:700;text-decoration:none">{e(G[code]["labels"]["guides"])}</a>'}<div class="langs">{langs}</div><a class="btn small" href="{go}" {rel} {ev(code, 'nav')}>{e(t['nav_cta'])}</a></nav>
</header>
<main>
<div class="hero">
  <div>
    <h1>{t['hero_h1']}</h1>
    <p class="lede">{e(t['hero_sub'])}</p>
    <p class="aud">{e(t['audience'])}</p>
    <a class="btn" href="{go}" {rel} {ev(code, 'hero')}>{e(t['cta'])}</a>
    <p class="note">{e(t['cta_note'])}</p>
  </div>
  <form class="invoice" id="calc" aria-labelledby="calc-h" onsubmit="return false">
    <div class="inv-head"><b id="calc-h">{e(t['invoice_label'])} · {e(t['calc_h2'])}</b>
      <label for="cur">{e(t['currency_label'])} <select id="cur">{opts}</select></label></div>
    <p class="ex intro">{e(t['calc_intro'])}</p>
    {rows}
    <div class="sum"><span>{e(t['total_month'])}</span><span id="tm"></span></div>
    <div class="sum year"><span>{e(t['total_year'])}</span><s id="ty"></s></div>
    <div class="sum free"><span>{e(t['free_plan_line'])}</span><span id="tf"></span></div>
    <div class="keep" id="keep" aria-live="polite"></div>
    <p class="ex" id="exnote">{e(t['calc_example_note'])}</p>
  </form>
</div>
<section aria-labelledby="plan-h">
  <h2 id="plan-h">{e(t['plan_h2'])}</h2>
  <dl class="facts">{facts}</dl>
  <p class="note">{e(t['plan_note'])}</p>
</section>
<section aria-labelledby="steps-h">
  <h2 id="steps-h">{e(t['steps_h2'])}</h2>
  <ol class="steps">{steps}</ol>
</section>
<section aria-labelledby="faq-h">
  <h2 id="faq-h">{e(t['faq_h2'])}</h2>
  <div class="faq">{faq}</div>
</section>
<section class="close" aria-labelledby="close-h">
  <h2 id="close-h">{e(t['cta2_h2'])}</h2>
  <p>{e(t['cta2_body'])}</p>
  <a class="btn" href="{go}" {rel} {ev(code, 'closing')}>{e(t['cta'])}</a>
</section>
</main>
<footer>
  <p>{e(t['disclosure'])}</p>
  <p>{e(t['independent'])}</p>
  <p>{e(t['checked'])}</p>
  <p>{'' if preview or code not in G else f'<a href="{gpath(code)}">{e(G[code]["labels"]["all_guides"])}</a> · '}{footer_links(code, preview)} · © 2026 SoloStarter HQ</p>
</footer>
</div>
<script>
(function(){{
  var L={json.dumps(t['htmllang'])}, KEEP={keep_tpl};
  var FX={json.dumps(FX)}, BASE={json.dumps(EXAMPLES_USD)}, RC={json.dumps(REGION_CURRENCY)};
  var ins=[].slice.call(document.querySelectorAll('#calc input')), cur=document.getElementById('cur'), prev=cur.value, region='';
  try{{var langs=(navigator.languages&&navigator.languages.length)?navigator.languages:[navigator.language];
    for(var i=0;i<langs.length&&!region;i++){{var m=/^[a-z]{{2,3}}-([A-Z]{{2}})$/i.exec(langs[i]||'');if(m)region=m[1].toUpperCase();}}}}catch(x){{}}
  var loc=region?L.split('-')[0]+'-'+region:L;
  function convert(from,to){{var a=FX[from],b=FX[to];ins.forEach(function(i){{var v=parseFloat(i.value);if(!isFinite(v)||v<=0)return;
    i.value=Math.max(b[1],Math.round(v*b[0]/a[0]/b[1])*b[1])}});prev=to}}
  function fmt(n){{try{{return new Intl.NumberFormat(loc,{{style:'currency',currency:cur.value,currencyDisplay:'narrowSymbol',maximumFractionDigits:0}}).format(n)}}catch(x){{return cur.value+' '+Math.round(n)}}}}
  function calc(){{
    var m=ins.reduce(function(a,i){{var v=parseFloat(i.value);return a+(isFinite(v)&&v>0?v:0)}},0);
    document.getElementById('tm').textContent=fmt(m);
    document.getElementById('ty').textContent=fmt(m*12);
    document.getElementById('tf').textContent=fmt(0);
    var k=document.getElementById('keep');k.textContent=KEEP.replace('{{amount}}',fmt(m*12));
    k.classList.add('bump');setTimeout(function(){{k.classList.remove('bump')}},180);
  }}
  if(region&&RC[region]&&RC[region]!==cur.value){{cur.value=RC[region];convert(prev,cur.value);}}
  ins.forEach(function(i){{i.addEventListener('input',calc)}});
  cur.addEventListener('change',function(){{convert(prev,cur.value);calc()}});calc();
}})();
</script>"""


def page(code):
    t = S[code]
    return f'<!doctype html>\n<html lang="{t["htmllang"]}">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n{head(code)}\n</head>\n<body>\n{body(code)}\n</body>\n</html>\n'


OWNER = {k: os.environ.get(k, "").strip() for k in ("OWNER_NAME", "OWNER_ADDRESS", "OWNER_EMAIL")}


LEGAL = json.load(open(os.path.join(HERE, "legal.json"), encoding="utf-8"))


PAGES = {"legal": "legal/", "privacy": "privacy/", "earn": "how-we-make-money/"}
NAME_LINE = {"en": "{NAME}, trading as SoloStarterHQ (sole trader)",
             "es": "{NAME}, que opera como SoloStarterHQ (empresario individual)",
             "pt-br": "{NAME}, atuando como SoloStarterHQ (empresário individual)",
             "de": "{NAME}, handelnd unter SoloStarterHQ (Einzelunternehmer)"}


def footer_links(code, preview=False):
    t, L = S[code], LEGAL[code]
    return " · ".join(f'<a href="{"#" if preview else "/" + t["path"] + PAGES[k]}">{e(label)}</a>'
                      for k, label in zip(("legal", "privacy", "earn"), L["footer_links"]))


def banner(code, preview=False):
    t, L = S[code], LEGAL[code]
    href = "#" if preview else "/" + t["path"] + PAGES["earn"]
    return f'<p class="adbar"><strong>{e(L["banner"])}</strong> <a href="{href}">{e(L["banner_link"])}</a></p>'


def legal(code, kind):
    t, L = S[code], LEGAL[code]
    P = L["pages"][kind]
    addr = ", ".join(x.strip() for x in OWNER["OWNER_ADDRESS"].split("|"))
    def fill(x):
        x = e(x.replace("{NAME_LINE}", NAME_LINE[code]))
        return (x.replace("{NAME}", e(OWNER["OWNER_NAME"])).replace("{ADDRESS}", e(addr))
                 .replace("{EMAIL}", f'<a href="mailto:{e(OWNER["OWNER_EMAIL"])}">{e(OWNER["OWNER_EMAIL"])}</a>')
                 .replace("{DIRECT}", f'<a href="{direct(code)}" rel="nofollow noopener">{direct(code).replace("https://", "")}</a>'))
    secs = "".join(f"<h2>{e(h)}</h2>" + "".join(f"<p>{fill(p)}</p>" for p in ps) for h, ps in P["sections"])
    return f"""<!doctype html>
<html lang="{t['htmllang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(P['title'])}</title><meta name="description" content="{e(P['h1'])}: SoloStarter HQ.">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{url(code)}{PAGES[kind]}"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONTS}
{analytics()}
<style>{CSS} main.legal{{max-width:44rem;padding-block:24px 56px}} main.legal h1{{font-size:clamp(1.7rem,4vw,2.2rem);margin-bottom:8px}} main.legal h2{{font-size:1.2rem;margin:32px 0 8px}} main.legal p{{color:var(--muted);margin:0 0 10px}} main.legal a{{color:var(--accent)}} .upd{{font-size:.85rem}}</style>
</head><body><div class="wrap">
<header class="top"><a class="brand" href="/{t['path']}">SoloStarter<span>HQ</span></a></header>
<main class="legal"><h1>{e(P['h1'])}</h1><p class="upd">{e(L['version'])}. {e(L['changes'])}</p>
{secs}
<p><a href="/{t['path']}">{e(L['back'])}</a></p></main>
<footer><p>{footer_links(code)} · © 2026 SoloStarter HQ</p></footer></div></body></html>
"""


def redirect(code):
    return f"""<!doctype html>
<html lang="{S[code]['htmllang']}"><head><meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta http-equiv="refresh" content="0; url={aff(code)}">
<title>SoloStarter HQ</title>
<link rel="canonical" href="{url(code)}">
<script>location.replace({json.dumps(aff(code))});</script>
</head><body><p><a href="{aff(code)}" rel="sponsored nofollow">Continue</a></p></body></html>
"""


# ---- Guides (content pages) ------------------------------------------------
# guides.json holds the guide pages per language. Every claim in them is grounded
# in systeme.io's own pages (see GUIDE_FACTS.md); every page carries the Ad label,
# the disclosure and several sign-up buttons.
G = json.load(open(os.path.join(HERE, "guides.json"), encoding="utf-8"))
# Translations live in guides.<lang>.json (same structure, same page ids).
import glob as _glob
for _f in sorted(_glob.glob(os.path.join(HERE, "guides.*.json"))):
    G.update(json.load(open(_f, encoding="utf-8")))
GUIDE_CSS = """
.crumbs{font-size:.85rem;color:var(--muted);margin:8px 0 0}.crumbs a{color:inherit}
.g-hero{padding-block:clamp(20px,4vw,48px) 8px;max-width:46rem}
.g-hero h1{font-size:clamp(2rem,4.6vw,3rem)}
.g-cta{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;margin-top:6px}
.g-body{display:grid;grid-template-columns:minmax(0,46rem) minmax(0,15rem);gap:clamp(24px,5vw,56px);align-items:start}
.g-body article section{padding-block:22px}.g-body article section+section{border-top:1px solid var(--line)}
.g-body h2{font-size:clamp(1.35rem,2.6vw,1.75rem);margin-bottom:10px}
.g-body p,.g-body li{max-width:42em}.g-body ul,.g-body ol{padding-left:1.3em}.g-body li{margin:6px 0}
.toc{position:sticky;top:16px;font-size:.88rem;border-left:3px solid var(--line);padding-left:14px}
.toc b{display:block;margin-bottom:6px}.toc a{display:block;color:var(--muted);text-decoration:none;padding:3px 0}.toc a:hover{color:var(--ink)}
.ctabox{background:var(--card);border:2px solid var(--accent);border-radius:14px;padding:20px;margin:26px 0}
.ctabox h3{font-size:1.25rem}.ctabox p{color:var(--muted);margin:6px 0 14px}
.copybox{border:1px dashed var(--line);border-radius:12px;padding:16px;margin:22px 0}
.copybox p{margin:0 0 8px}.copyrow{display:flex;gap:8px;flex-wrap:wrap}.copyrow input{flex:1 1 16rem;min-width:0;font:500 .85rem/1.4 var(--mono)}
.copyrow button{font:700 .9rem/1 var(--body);background:var(--ink);color:var(--paper);border:0;border-radius:8px;padding:10px 14px;cursor:pointer}
.cards{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));gap:14px;margin:16px 0 0}
.cards a{display:block;height:100%;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;color:var(--ink);text-decoration:none}
.cards a:hover{border-color:var(--accent)}.cards b{display:block;font:700 1.05rem/1.3 var(--display);margin-bottom:6px}.cards span{color:var(--muted);font-size:.92rem}
.sources{font-size:.85rem;color:var(--muted)}.sources a{color:inherit;word-break:break-all}
.picker{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;margin-top:18px}
.picker label{display:flex;gap:10px;align-items:center;padding:8px 0;cursor:pointer}.picker input{width:1.1rem;height:1.1rem;accent-color:var(--accent)}
.picker button{margin-top:10px;font:700 1rem/1 var(--body);background:var(--ink);color:var(--paper);border:0;border-radius:10px;padding:12px 18px;cursor:pointer}
#pick-out{margin-top:14px}
.sticky{position:fixed;left:0;right:0;bottom:0;z-index:5;display:flex;gap:10px;align-items:center;background:var(--ink);color:var(--paper);padding:10px 14px calc(10px + env(safe-area-inset-bottom,0px))}
.sticky span{flex:1;font-size:.9rem}.sticky .btn{padding:10px 14px;font-size:.9rem}.sticky button{background:none;border:0;color:var(--paper);font-size:1.3rem;cursor:pointer}
[hidden]{display:none!important}
@media (min-width:900px){.sticky{display:none!important}}
@media (max-width:900px){.g-body{grid-template-columns:1fr}.toc{display:none}}
"""


def guide_langs():
    return [c for c in LANGS if c in G]


def gurl(code, slug=None):
    return f"{BASE}/{S[code]['path']}{G[code]['dir']}{slug + '/' if slug else ''}"


def gpath(code, slug=None):
    return f"/{S[code]['path']}{G[code]['dir']}{slug + '/' if slug else ''}"


def pid(p):
    """A guide's id is the same in every language; its slug is translated."""
    return p.get("id", p["slug"])


def slug_for(code, gid):
    for p in G[code]["pages"]:
        if pid(p) == gid:
            return p["slug"]
    return None


def guide_alts(gid):
    langs = [c for c in guide_langs() if gid is None or slug_for(c, gid)]
    a = "".join(f'<link rel="alternate" hreflang="{S[c]["hreflang"]}" href="{gurl(c, None if gid is None else slug_for(c, gid))}">' for c in langs)
    if "en" in langs:
        a += f'<link rel="alternate" hreflang="x-default" href="{gurl("en", None if gid is None else slug_for("en", gid))}">'
    return a


def guide_head(code, title, desc, canonical, slug, ld):
    t = S[code]
    return f"""<!doctype html>
<html lang="{t['htmllang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">{guide_alts(slug)}
<meta property="og:type" content="article"><meta property="og:site_name" content="SoloStarter HQ">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}/og.png">
<meta property="og:locale" content="{t['og_locale']}"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1d6b4a"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONTS}
{analytics()}
{''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)}
<style>{CSS}{GUIDE_CSS}</style>
</head><body>"""


def guide_top(code):
    t, L = S[code], G[code]["labels"]
    rel = 'rel="sponsored nofollow noopener"'
    return f"""{banner(code)}<div class="wrap">
<header class="top">
  <a class="brand" href="/{t['path']}">SoloStarter<span>HQ</span></a>
  <nav aria-label="{e(L['guides'])}"><a href="{gpath(code)}" style="color:var(--ink);font-weight:700;text-decoration:none">{e(L['guides'])}</a><a class="btn small" href="/go/{code}/" {rel} {ev(code, 'guide-nav')}>{e(t['nav_cta'])}</a></nav>
</header>"""


def guide_cta(code, where, cls="btn"):
    t = S[code]
    return f'<a class="{cls}" href="/go/{code}/" rel="sponsored nofollow noopener" {ev(code, where)}>{e(t["cta"])}</a>'


def guide_bottom(code, page_id):
    t, L = S[code], G[code]["labels"]
    return f"""
<footer>
  <p>{e(t['disclosure'])}</p>
  <p>{e(t['independent'])}</p>
  <p>{e(L['updated'])} {e(t['checked'])}</p>
  <p><a href="{gpath(code)}">{e(L['all_guides'])}</a> · {footer_links(code)} · © 2026 SoloStarter HQ</p>
</footer>
</div>
<div class="sticky" id="sticky" hidden><span>{e(L['sticky'])}</span><a class="btn" href="/go/{code}/" rel="sponsored nofollow noopener" {ev(code, 'sticky')}>{e(L['sticky_btn'])}</a><button type="button" id="sticky-x" aria-label="{e(L['close'])}">×</button></div>
<script>
(function(){{
  var b=document.getElementById('copy-btn'),i=document.getElementById('copy-url');
  if(b&&i){{b.addEventListener('click',function(){{var done=function(){{b.textContent={json.dumps(L['copy_done'])};if(window.umami)umami.track('referral-copy',{{lang:{json.dumps(code)},page:{json.dumps(page_id)}}});setTimeout(function(){{b.textContent={json.dumps(L['copy_btn'])}}},2500)}};
    if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(i.value).then(done,function(){{i.select()}});else{{i.select();try{{document.execCommand('copy');done()}}catch(x){{}}}}}});i.addEventListener('focus',function(){{i.select()}});}}
  var s=document.getElementById('sticky'),x=document.getElementById('sticky-x'),off=false;
  try{{off=sessionStorage.getItem('ssq-bar')==='off'}}catch(err){{}}
  if(s&&!off&&'IntersectionObserver' in window){{var tgt=[].slice.call(document.querySelectorAll('.g-cta,.ctabox')),seen=tgt.map(function(_,n){{return n===0}});
    var up=function(){{s.hidden=off||seen.some(Boolean)}};
    var io=new IntersectionObserver(function(es){{es.forEach(function(en){{seen[tgt.indexOf(en.target)]=en.isIntersecting}});up()}});tgt.forEach(function(t){{io.observe(t)}});
    x.addEventListener('click',function(){{off=true;try{{sessionStorage.setItem('ssq-bar','off')}}catch(err){{}}up()}});}}
}})();
</script>
</body></html>
"""


def copybox(code):
    L = G[code]["labels"]
    return f"""<div class="copybox"><p><b>{e(L['copy_h'])}</b></p><div class="copyrow"><input id="copy-url" type="text" readonly value="{e(aff(code))}" aria-label="{e(L['copy_h'])}"><button type="button" id="copy-btn">{e(L['copy_btn'])}</button></div><p class="note">{e(L['copy_note'])}</p></div>"""


def ctabox(code, where):
    L = G[code]["labels"]
    return f"""<aside class="ctabox"><h3>{e(L['cta_box_h'])}</h3><p>{e(L['cta_box_p'])}</p>{guide_cta(code, where)}<p class="note">{e(S[code]['cta_note'])}</p></aside>"""


def render_section(sec, i):
    h = f'<section id="s{i}"><h2>{e(sec["h2"])}</h2>'
    for p in sec.get("p", []):
        h += f"<p>{e(p)}</p>"
    if sec.get("ul"):
        h += "<ul>" + "".join(f"<li>{e(x)}</li>" for x in sec["ul"]) + "</ul>"
    if sec.get("ol"):
        h += "<ol>" + "".join(f"<li>{e(x)}</li>" for x in sec["ol"]) + "</ol>"
    if sec.get("after"):
        h += f"<p>{e(sec['after'])}</p>"
    return h + "</section>"


def guide_page(code, g):
    t, L = S[code], G[code]["labels"]
    pages = {pid(p): p for p in G[code]["pages"]}
    canonical = gurl(code, g["slug"])
    crumbs = [("SoloStarter HQ", f"{BASE}/{t['path']}"), (L["guides"], gurl(code)), (g["h1"], canonical)]
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]},
        {"@context": "https://schema.org", "@type": "Article", "headline": g["h1"], "description": g["desc"], "inLanguage": t["htmllang"],
         "dateModified": "2026-10-13", "author": {"@type": "Organization", "name": "SoloStarter HQ"}, "mainEntityOfPage": canonical},
        {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": t["htmllang"], "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faq"]]},
    ]
    secs = g["sections"]
    body = ""
    for i, sec in enumerate(secs):
        body += render_section(sec, i)
        if i == 1:
            body += ctabox(code, "guide-mid")
    toc = "".join(f'<a href="#s{i}">{e(sec["h2"])}</a>' for i, sec in enumerate(secs))
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in g["faq"])
    related = "".join(f'<li><a href="{gpath(code, pages[r]["slug"])}"><b>{e(pages[r]["h1"])}</b><span>{e(pages[r]["card"])}</span></a></li>' for r in g["related"] if r in pages)
    srcs = "".join(f'<li><a href="{u}" rel="nofollow noopener">{e(u.replace("https://", ""))}</a></li>' for u in g["sources"])
    return guide_head(code, g["title"], g["desc"], canonical, pid(g), ld) + guide_top(code) + f"""
<main>
<p class="crumbs"><a href="/{t['path']}">SoloStarter HQ</a> › <a href="{gpath(code)}">{e(L['guides'])}</a></p>
<div class="g-hero">
  <h1>{e(g['h1'])}</h1>
  <p class="lede">{e(g['lede'])}</p>
  <div class="g-cta">{guide_cta(code, 'guide-top')}</div>
  <p class="note">{e(t['cta_note'])}</p>
</div>
<div class="g-body">
<article>
{body}
<section id="faq"><h2>{e(L['faq_h2'])}</h2><div class="faq">{faq}</div></section>
{ctabox(code, 'guide-end')}
{copybox(code)}
<section><h2>{e(L['related_h2'])}</h2><ul class="cards">{related}</ul></section>
<section class="sources"><h2>{e(L['sources_h2'])}</h2><p>{e(L['sources_intro'])}</p><ul>{srcs}</ul></section>
</article>
<nav class="toc" aria-label="{e(L['on_this_page'])}"><b>{e(L['on_this_page'])}</b>{toc}<a href="#faq">{e(L['faq_h2'])}</a></nav>
</div>
</main>""" + guide_bottom(code, g["slug"])


def guide_hub(code):
    t, L, H = S[code], G[code]["labels"], G[code]["hub"]
    pages = G[code]["pages"]
    canonical = gurl(code)
    ld = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "SoloStarter HQ", "item": f"{BASE}/{t['path']}"},
            {"@type": "ListItem", "position": 2, "name": L["guides"], "item": canonical}]},
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": H["h1"], "description": H["desc"], "inLanguage": t["htmllang"], "url": canonical},
    ]
    byslug = {pid(p): p for p in pages}
    goals = "".join(f'<label><input type="checkbox" value="{k}"> {e(label)}</label>' for k, label, _ in H["goals"])
    gmap = {k: [{"href": gpath(code, byslug[s]["slug"]), "t": byslug[s]["h1"]} for s in sl if s in byslug] for k, _, sl in H["goals"]}
    cards = "".join(f'<li><a href="{gpath(code, p["slug"])}"><b>{e(p["h1"])}</b><span>{e(p["card"])}</span></a></li>' for p in pages)
    return guide_head(code, H["title"], H["desc"], canonical, None, ld) + guide_top(code) + f"""
<main>
<div class="g-hero">
  <h1>{e(H['h1'])}</h1>
  <p class="lede">{e(H['lede'])}</p>
  <div class="g-cta">{guide_cta(code, 'hub-top')}</div>
  <p class="note">{e(t['cta_note'])}</p>
</div>
<section aria-labelledby="pick-h"><h2 id="pick-h">{e(H['pick_h2'])}</h2><p class="sec-intro">{e(H['pick_intro'])}</p>
<form class="picker" id="picker" onsubmit="return false">{goals}<button type="submit">{e(H['pick_btn'])}</button><div id="pick-out" aria-live="polite"></div></form></section>
<section aria-labelledby="all-h"><h2 id="all-h">{e(H['all_h2'])}</h2><ul class="cards">{cards}</ul></section>
{ctabox(code, 'hub-end')}
{copybox(code)}
</main>
<script>
(function(){{var M={json.dumps(gmap, ensure_ascii=False)},f=document.getElementById('picker'),o=document.getElementById('pick-out');
f.addEventListener('submit',function(){{var seen={{}},list=[];[].slice.call(f.querySelectorAll('input:checked')).forEach(function(c){{(M[c.value]||[]).forEach(function(x){{if(!seen[x.href]){{seen[x.href]=1;list.push(x)}}}})}});
o.textContent='';if(!list.length){{o.textContent={json.dumps(H['pick_none'])};return}}
var p=document.createElement('p');p.innerHTML='<b></b>';p.firstChild.textContent={json.dumps(H['pick_result'])};o.appendChild(p);var ul=document.createElement('ul');
list.forEach(function(x){{var li=document.createElement('li'),a=document.createElement('a');a.href=x.href;a.textContent=x.t;li.appendChild(a);ul.appendChild(li)}});o.appendChild(ul);
if(window.umami)umami.track('guide-picker',{{lang:{json.dumps(code)},goals:[].slice.call(f.querySelectorAll('input:checked')).map(function(c){{return c.value}}).join(',')}});}});}})();
</script>""" + guide_bottom(code, "hub")


def write_guides(out):
    urls = []
    for c in guide_langs():
        base_dir = os.path.join(out, S[c]["path"], G[c]["dir"])
        os.makedirs(base_dir, exist_ok=True)
        open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8").write(guide_hub(c))
        urls.append((gurl(c), "hub"))
        for g in G[c]["pages"]:
            d = os.path.join(base_dir, g["slug"])
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(guide_page(c, g))
            urls.append((gurl(c, g["slug"]), pid(g)))
    return urls


def main():
    missing = [k for k, v in OWNER.items() if not v]
    if missing and not os.environ.get("ALLOW_MISSING"):
        sys.exit("Missing legal details: " + ", ".join(missing) + ". Set them before building for launch.")
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    for c in LANGS:
        d = os.path.join(OUT, S[c]["path"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(c))
        for kind, slug in PAGES.items():
            os.makedirs(os.path.join(d, slug), exist_ok=True)
            open(os.path.join(d, slug, "index.html"), "w", encoding="utf-8").write(legal(c, kind))
        g = os.path.join(OUT, "go", c)
        os.makedirs(g, exist_ok=True)
        open(os.path.join(g, "index.html"), "w", encoding="utf-8").write(redirect(c))
    guide_urls = write_guides(OUT)
    shutil.copytree(os.path.join(HERE, "static"), OUT, dirs_exist_ok=True)
    # sitemap with hreflang alternates
    alts = "".join(f'<xhtml:link rel="alternate" hreflang="{S[c]["hreflang"]}" href="{url(c)}"/>' for c in LANGS)
    alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{url("en")}"/>'
    urls = "".join(f"<url><loc>{url(c)}</loc><lastmod>2026-10-12</lastmod>{alts}</url>" for c in LANGS)
    urls += "".join(f"<url><loc>{u}</loc><lastmod>2026-10-13</lastmod></url>" for u, _ in guide_urls)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
        + urls + "</urlset>\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nDisallow: /go/\nSitemap: {BASE}/sitemap.xml\n")
    open(os.path.join(OUT, "favicon.svg"), "w").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1d6b4a"/><text x="32" y="44" font-family="Arial,sans-serif" font-size="34" font-weight="700" text-anchor="middle" fill="#ffd84a">S</text></svg>')
    open(os.path.join(OUT, "404.html"), "w").write(
        f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | SoloStarter HQ</title></head>'
        f'<body style="font-family:system-ui;padding:40px 16px;max-width:40rem;margin:auto"><h1>Page not found</h1><p><a href="/">English</a> · <a href="/es/">Español</a> · <a href="/pt-br/">Português</a> · <a href="/de/">Deutsch</a></p></body></html>')
    # preview body for the artifact (no document wrapper)
    open(os.path.join(OUT, "..", "preview.html"), "w", encoding="utf-8").write(
        "\n".join(f'<template id="t-{c}"></template>' for c in []) + head("en", True).replace("<title>" + e(S["en"]["title"]) + "</title>", "<title>SoloStarter HQ Preview</title>") + "\n" + body("en", True))
    if PREFIX:
        for dp, _, fs in os.walk(OUT):
            for f in fs:
                if f.endswith(".html"):
                    fp = os.path.join(dp, f)
                    t = open(fp, encoding="utf-8").read()
                    t = t.replace('href="/', f'href="{PREFIX}/').replace('src="/', f'src="{PREFIX}/')
                    open(fp, "w", encoding="utf-8").write(t)
    print("built", OUT)


if __name__ == "__main__":
    main()
