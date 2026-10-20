# Guide pages: facts sheet

Every claim in `guides.json` comes from systeme.io's own pages, read word for word in a
browser on 13 October 2026 (not a summary). If it isn't on systeme.io's site, it doesn't go
on ours. Where systeme.io's pages contradict each other, the claim is left out.

## Rules from the affiliate agreement (systeme.io/affiliate-agreement)
- "you may not use any other competitor trademarks in your promotion of systeme.io" → no competitor names anywhere (seo_check.py blocks a list of them).
- "You must not use our trademark in a misleading way or imply that we endorse, sponsor or approve of your services" → independence line on every page.
- "Once a lead signs up for a free account using your affiliate link, you become their affiliate for life" and "If a lead clicks your affiliate link but never signs up for a free account, no referral is recorded" → every CTA goes to the free sign-up page.
- 60% commission; customer must stay 30 days; no self-referrals.

## Pricing page (systeme.io/pricing, FAQ "Last updated: April 2026")
- "Systeme.io has four plans based primarily on contact limits. Free: 2,000 contacts, 3 sales funnels, 1 course. Startup ($17/month): 5,000 contacts, 10 sales funnels, 5 courses. Webinar ($47/month): 10,000 contacts, 50 sales funnels, 20 courses, plus evergreen webinars. Unlimited ($97/month): unlimited contacts, funnels, courses and automation rules. All plans include unlimited email sends, unlimited sub-accounts, 0% transaction fees, and the same set of core tools."
- "the free plan supports up to 2,000 contacts, 3 sales funnels, 1 blog, 1 course, 1 affiliate program, and 1 custom domain. Emails sent are unlimited. The free plan never expires and does not require a credit card. Other features have lower limits on the free plan, like 1 automation rule, 1 email campaign and 500 students."
- "Under 2,000 contacts: use the free plan. It costs nothing and covers most needs. 2,000 to 5,000 contacts: Startup at $17/month."
- Annual billing: "2 MONTHS FREE".
- Cancel: "you keep your current plan until your next billing date, then your account reverts to the free plan."
- Integrations listed: Stripe, Apple Pay, PayPal, Razorpay, Flutterwave, Mercado Pago, Xendit, Cash on delivery. "No transaction fees — Accept payments using Stripe or PayPal at no extra cost".
- Cost of separate tools: "systeme.io covers all of this on the free plan or for $17/month" (the competitor names in that answer are NOT used).
- **Not used (contradiction):** student limits. The FAQ says 500 students on free; the same page says "Unlimited students" on all plans, and the courses page says "∞ Students supported".

## Sales funnels (systeme.io/sales-funnels)
- Definition: "a sequence of pages that guides a visitor from their first contact with your business to a purchase"; typical opt-in, sales, checkout, thank-you pages; "visitors move through it at any time of day, without you being present".
- Six steps to a first funnel (Funnels → Create a funnel → type/template → edit → connect payment processor → email automation → Publish); "Most first funnels can be live in under 2 hours."
- Templates: "lead magnet, product launch, webinar registration, tripwire, membership site". Deadline funnels ("Offer ended" page), A/B tests, stats (page views, opt-in rates, sales), Stripe or PayPal, upsell and downsell offers.
- "a purchase in your funnel automatically delivers the product, adds the buyer to your email list, and tracks affiliates"; one funnel can sell a digital product, grant course access, book a coaching session and enrol in an email sequence.

## Email marketing (systeme.io/email-marketing)
- Broadcasts, automated sequences, tagging, scheduling, segmentation, drag-and-drop editor (or classic editor), A/B tests for subject lines, stats on opens, clicks and sales.
- "The free plan includes unlimited email sends to up to 2,000 contacts. There is no daily or monthly send cap."
- Subscribers added automatically from forms; sequences triggered by opt-in, purchase or course module completion.
- Trade-off used without names: specialist email tools "have more advanced email design tools".

## Marketing automation (systeme.io/marketing-automation)
- Rules (trigger "Form subscribed" + action "Subscribe to campaign") and visual workflows with delays, conditions, branching. Triggers: signing up, purchase, clicking a link, a tag, a date. Actions: send emails, grant course access, update tags, move to a funnel. Drag-and-drop, no coding or API keys.

## Online courses (systeme.io/online-courses)
- Modules and lectures, drip (day-by-day or week-by-week), quizzes with automatic grading, bundles, progress tracking, instant access on purchase, contacts added automatically, 0% transaction fees.
- Video: FAQ says "embed videos hosted on YouTube, Vimeo, or Wistia" (used); the same page also says "Host your videos directly on systeme.io" (contradiction: not used).
- "systeme.io does not have native certificate generation".

## Booking calendar (systeme.io/booking-calendar)
- Booking page, 1-on-1 and group events, availability, buffer times, max bookings per day, 2-way Google Calendar sync, Zoom and Google Meet links, confirmation and reminder emails, contact added to CRM.
- "Payment collection at time of booking is also available on the free plan via Stripe or PayPal"; full payment or deposit; 0% transaction fees.
- Limits: not advanced team scheduling or complex intake forms; "no automated import of past appointments".

## Website builder (systeme.io/website-builder)
- Templates, drag-and-drop, pages and navigation, SEO titles and descriptions per page, multilingual pages, blog with categories, tags and SEO settings.
- Free plan: "1 custom domain on the free plan ... No hosting fee, no plugin charges, and no storage limits."
- Editor "entirely visual"; custom CSS possible "but it is never required". Sales pages are built in the funnel builder and can be linked from the site's navigation.
- Trade-off used without names: other builders have "more design templates".

## Free migration (systeme.io/free-migration)
- Included "with the Unlimited monthly plan ($97/month) or any annual plan"; team moves funnels, pages, email lists, sequences, courses, customer records.

## Translations (es, pt-br, de; checked 13 Oct 2026)
- `guides.<lang>.json` translate `guides.json` page for page. Checked before publishing: same sections, FAQs, related pages and sources as the English; every figure matches; only systeme.io links; no affiliate IDs in the text; no competitor names; German uses the formal "Sie".
- Each language's buttons and copy box go to systeme.io's sign-up page in that language (`/go/<lang>/` → systeme.io/es/, /pt/, /de/), with the same affiliate ID.
- The facts come from systeme.io's English pages, and each page says so in its sources note.

## Feature guides added 20 October 2026 (read word for word in Chrome on 20 Oct 2026)

Ten English guides: affiliate-program, evergreen-webinars, creator-store, crm-pipelines,
online-community, physical-products, sms-marketing, sub-accounts, white-label, free-migration.
Each sentence that states a feature, limit or price is attributed ("systeme.io says") or taken
from the pricing table. Usage ideas ("you could…") only combine features the pages confirm.

### Affiliate management (systeme.io/affiliate-management)
- Settings: commission percentage, payout delay, minimum payout amount, second-tier commissions. `{affiliate_id}` email variable.
- Invoices generated automatically on the 10th of each month; affiliates choose wire transfer or PayPal; connect Wise to pay everyone at once, or pay individually.
- Included on all plans including free; no per-affiliate fee; setup about 10 minutes.
- **Not used:** "instantly" (payment is a manual step); the FAQ's "up to 1 product" on free (pricing page says "1 affiliate program": different wording, so no number is given).

### Automated (evergreen) webinars (systeme.io/automated-webinars)
- Registration, broadcast and replay page templates; drag and drop; reminder emails with unique access links; timed Buy Now buttons, banners, scarcity timers; replay management.
- Buyer enrolled automatically and removed from the no-purchase sequence. Setup typically 2 to 4 hours. Not suited to live interactive webinars.
- Pricing table: evergreen webinars 0 / 0 / 10 / Unlimited (Free / Startup / Webinar $47 / Unlimited $97).
- **Not used (contradiction):** schedule options. The page says "hourly, daily or instantly", the FAQ "every 15 minutes, hourly or daily". Only "hourly or daily" is used.

### Creator store (systeme.io/creator-store)
- Link-in-bio store selling digital products, courses, physical products, coaching and affiliate links to external sites; templates, custom sections, Subscribe card for leads and lead magnets, SEO settings; yourname.systeme.io or a custom domain; basic store about 20 minutes.
- Free plan: 2,000 contacts, 1 custom domain; paid plans from $17; 0% transaction fees.
- Pricing table: mobile-optimized link-in-bio page 1 / 3 / 10 / Unlimited.
- **Not used:** "up to 3 payment links", "without leaving the page", "no payment processor setup".

### CRM pipelines (systeme.io/crm-pipelines)
- Kanban board, custom stages, drag and drop, internal notes, multiple pipelines (CRM → "Create a pipeline"), team collaboration.
- Automation rules add or move deals on subscribe, link click, purchase or form submission. Same contacts as the email lists, no syncing. Included on all plans within the contact limit.
- Pricing table: CRM pipelines 1 / 5 / 20 / 100; automation rules 1 / 10 / 100 / Unlimited.
- Booking calendar page: new bookings are added to contacts.

### Online communities (systeme.io/online-communities)
- Private or public; posts, comments, file uploads, voice memos, YouTube and Loom embeds; topics, pinned posts, search, scheduled posts, post approval; custom domain, name, cover image.
- Sold through funnels as a digital product on an order form, one-time or subscription; access granted on purchase and removed on cancellation; 0% transaction fees; no per-member fee.
- No branded mobile app; posts can't be migrated from an existing social media group (the page names the platform; we don't).
- Pricing table: communities 1 / 5 / 20 / Unlimited; members unlimited on all plans.

### Physical products (systeme.io/physical-products)
- Variants (size, color, material) with automatic SKUs; real-time inventory; shipping fees by weight, order price, quantity or customer location, with delivery zones and carrier rates; "Physical Product" element for order forms and sales pages; order filtering by date, status or product.
- Sale flow: create under Products → add to a funnel step or website page → Stripe or PayPal → order dashboard; upsells and post-purchase email sequences on the same platform.
- Suits a limited product range sold through funnels (merchandise, physical books); not large-scale retail with deep catalogue management or complex warehouse integrations.
- No automated product import: contacts via CSV, listings recreated by hand; migration team helps on Unlimited or annual plans.
- Pricing table: physical products unlimited; variants 50 / 100 / 250 / Unlimited; shipping management, inventory management and cash on delivery listed (per-plan ticks not shown in the page text, so no plan claim is made).
- **Not used:** comparisons with named shop platforms.

### SMS marketing (systeme.io/sms-marketing)
- Twilio integration (paste SID and Auth Token); templates with {first_name} or {email}; SMS steps in automation rules and workflows; triggers such as a purchase, a tag, a timed delay; email + SMS in one workflow (example: welcome email day 0, SMS day 1, follow-up email day 3); confirmation text when a client buys a course; delivery and failure reports.
- Feature included at no extra charge; Twilio charges per message by destination country; paid to Twilio directly, no systeme.io mark-up.
- Compliance is the owner's responsibility: explicit opt-in, opt-out instructions ("Reply STOP to unsubscribe") required by Twilio.
- Two-way conversations, shortcodes or SMS-first campaigns: a dedicated tool may be more appropriate.
- **Not used:** the Twilio per-message dollar figure (a third party's price); the FAQ answer saying "All features are available on every plan" (contradicts the pricing table for webinars).

### Sub-accounts (systeme.io/sub-accounts)
- Separate workspaces with their own funnels, contacts, email sequences, products, settings and payment gateways; one-click creation; switching from the main dashboard without separate logins; invite team members and clients; full admin or restricted assistant access; share funnels and emails between sub-accounts; per-sub-account dashboard.
- Unlimited on all plans including free; "the same limits as your main account"; no per-client fees. Free migration (Unlimited or annual) can assist; client sites stay live until you switch.
- Pricing table: sub-accounts unlimited; assistant accounts unlimited on all plans.
- **Not used:** "one systeme.io Unlimited plan covers all clients" (sits awkwardly with "available on all plans").

### White label (systeme.io/white-label, "Last updated: August 2026")
- Custom domain, logo, brand colours with live preview, sender email; branding on dashboards, login pages, transactional emails.
- Own monthly and annual plans, multiple languages and currencies; prices can't be lower than systeme.io's; no fee, commission or transaction fees; keep 100% of revenue.
- Resale by plan: Startup → Startup; Webinar → Startup and Webinar; Unlimited → all plans; Free → free white-label accounts.
- Ready-made website (homepage, pricing page, login/sign-up); funnels and automation rules create free white-label accounts on subscribe; reseller dashboard (active plans, revenue, leads; search, filter, block, impersonate).
- Best for agencies, consultants, entrepreneurs; not ideal for heavy customisation, dedicated infrastructure, missing features; can't modify the underlying code. Existing clients can be invited to create accounts.
- **Not used:** the "$200,000 / 12 to 24 months" build-cost estimate.

### Free migration and free DNS setup (systeme.io/free-migration, systeme.io/free-dns-setup)
- Migration included with the Unlimited monthly plan ($97/month) or any annual plan. Three steps: sign up, contact support with setup details (screenshots, export files, read-only login where available), estimate then migration.
- Table rows used (only those with explicit notes): funnels and landing pages rebuilt; digital products with pricing and checkout pages; email lists with tags where possible; sequences and automations rebuilt; courses and membership content; customer and student records as CRM contacts; affiliate program structure; custom domain with DNS setup support. Payment/transaction history stays with the original processor.
- Simple migration 2 to 5 business days; larger 1 to 2 weeks; written estimate. No downtime; old platform stays live; no data deleted from it. Unsure platforms: contact support before signing up.
- DNS: buy a domain from any registrar, contact support with registrar login details, the team configures it and notifies you. A domain replaces the default systeme.io subdomain and lets you send from info@yourdomain.com, "essential for improving your email deliverability".
- **Not used:** the list of platforms the team migrates from (competitor names); the "Blog posts" row (no clear inclusion in the page text).

### Template library (systeme.io/templates)
- Checked but not used for a guide: the page is a filterable gallery with no feature text to quote.

### Translations of the feature guides (es, pt-br, de; 20 Oct 2026)
- The 10 feature guides are translated page for page in `guides.<lang>.json`, with the same `id` as the English so hreflang, related cards and `[[id|text]]` links line up.
- Checked by script before publishing: same number of sections, paragraphs, list items and FAQs as the English; identical link targets and inline affiliate link; identical figures; same related pages and sources; no URLs or affiliate IDs in the text; German uses "Sie"; Portuguese uses "a systeme.io"; titles ≤ 60 and descriptions 70–160 characters.
- Conventions kept from the first translations: es "Según systeme.io", prices "17 $ al mes", plan "Ilimitado"; pt-br "Segundo a systeme.io", "US$ 17 por mês", plan "Ilimitado"; de "Laut systeme.io", "17 $ im Monat", "Unlimited-Tarif". Inline ad label matches each language's banner: Publicidad, Publicidade, Werbung.
