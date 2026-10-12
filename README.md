# SoloStarter HQ

Landing pages for the systeme.io free plan, aimed at freelancers, in English, Spanish, Brazilian Portuguese and German. Every "Start free" button goes through `/go/<lang>/`, which forwards to Pras's systeme.io affiliate link.

## How it works

- `strings.json` holds all the words for every language. Add a language by adding a block.
- `build.py` turns one template into all the pages, the legal pages, the redirects, `sitemap.xml` and `robots.txt`.
- `seo_check.py` runs on every deploy and stops it if any page fails (title and description lengths, one H1, canonical, hreflang, structured data, sponsored links, legal pages).
- `.github/workflows/deploy.yml` builds and publishes to GitHub Pages on every push to `main`.

## Settings

The site address and the legal-page details are set in the workflow's `env` block. When solostarterhq.com is connected, change `SITE_BASE` to `https://solostarterhq.com` and add the domain under Settings → Pages.

## Rules

- No competitor brand names (systeme.io affiliate agreement).
- Name systeme.io next to sign-up buttons, and keep the "Ad" label and disclosure.
- Every claim about the plan must be checkable on systeme.io's own pages.

© 2026 SoloStarterHQ. All rights reserved.
