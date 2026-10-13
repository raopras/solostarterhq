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
