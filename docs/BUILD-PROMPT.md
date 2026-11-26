# Learning-Express — Phase-wise Build Prompt

**Concept:** *The express lane to free learning.* A free, AdSense-monetized learning hub that turns the best open-education resources into 12 guided "Express Lines" (transit-map metaphor: lines → stations), wrapped in study tools, a daily quiz, auto-updated video/news feeds, and a high-intent education lead-generation funnel ("Program Match").

**Why this idea wins:** education/online-degree/bootcamp keywords are among the highest-CPC AdSense niches; Program Match leads (degree, bootcamp, certificate, tutoring) are resellable to education partners; tools + daily quiz create repeat visits; original guides satisfy AdSense content requirements.

---

## Phase 0 — Guardrails (apply to every phase)
- Static HTML/CSS/vanilla JS only; must run on GitHub Pages free plan from `main` branch root. No build server.
- AdSense head tag on every page: `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>`; `ads.txt` = `google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0`.
- Top ribbon on every page: "Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership" → the owner's partner-contact page (URL assembled in JS, never in page source).
- All forms → FormSubmit AJAX to the owner inbox; the address is encoded in JS and never appears in HTML or as plain text anywhere.
- Brand is always "Learning-Express" (hyphenated). Never imply affiliation with EBSCO "LearningExpress". Disclosure in footer + `disclaimer.html`.
- AdSense policy: original content, privacy policy with Google cookie disclosure, about/contact pages, clear navigation, no prohibited content, no ad-click inducements.

## Phase 1 — Research & positioning
Open and read 38+ leading education sites (Khan, Coursera, edX, Quizlet, freeCodeCamp, Varsity Tutors, Wyzant, W3Schools, Alison, etc.). Record function, forms, monetization and design. Output `docs/RESEARCH.md` with adopted patterns and the trademark finding.

## Phase 2 — Design system
Transit-map identity: ink navy `#0E1330`, express blue `#1F5BFF`, signal orange `#FF5A1F`, lime `#B8F24A`, one color per line. Fonts: Bricolage Grotesque (headings), Inter (body), JetBrains Mono (labels). Light/dark mode, responsive grid, cards, station timeline component, funnel component, cookie banner, modal, toast, sticky mobile CTA. Accessibility: skip link, focus rings, reduced-motion support.

## Phase 3 — Generator & layout
Python generator (`build/build.py`) with a shared head/header/footer (`build/layout.py`): SEO meta, canonical, Open Graph, JSON-LD (WebSite, EducationalOrganization, Course, Article, FAQPage), consent-aware AdSense, nav, footer with independence notice. Outputs flat HTML at repo root + `sitemap.xml`, `robots.txt`, `data/search.json`.

## Phase 4 — Core content (AdSense-grade)
- 12 Express Lines × 6 stations (time estimate, description, 1–3 reputable free resources, progress checkbox), intro, destination, FAQ, auto-filled videos, next-line link, Program Match sidebar.
- 10 original long-form guides (Express Method, Active Recall, Spaced Repetition, Feynman, Pomodoro, Free Certificates, Choosing an Online Program, Weekly Plan, Learning with AI, Career Switch).
- About, Contact, Privacy (AdSense wording), Terms (contest + donation clauses), Disclaimer & Trademark.

## Phase 5 — Interactive engagement
Study tools (flashcards, Pomodoro timer, spaced-review scheduler with .ics export, GPA, final-grade-needed, reading speed, typing speed, goal-hours), Daily Quiz (deterministic daily set from a 72-question original bank, topic practice, streaks, share), network-map SVG, site search, printable 30-Day Planner.

## Phase 6 — Lead generation (highest priority for revenue)
`match.html`: 7-step funnel (goal → field → education level → format → budget → timeline → contact), deep-link prefill (`?goal=`, `?field=`), progress bar, trust badges, optional partner-consent checkbox, client-side lead score (HOT/WARM/NURTURE) in the submission subject, instant personalised result + free starter line. Secondary capture: newsletter strips, exit-intent 30-Day Planner modal, quiz-end signup, partner brief form.

## Phase 7 — Community & monetization pages
- `support.html`: one-time/monthly tiers ($5/$25/$100/$500), purpose selector (operations, promotions & marketing, hiring talent, contests & prizes, scholarships), allocation bars, pledge → secure payment link by email.
- `contests.html`: 3 monthly skill contests from `data/contests.json`, prizes, judging criteria, entry form, official-rules summary.
- `careers.html`: 6 roles + talent-pool application.
- `partners.html`: sponsorship/ads/education-partner packages + brief form.

## Phase 8 — Self-updating automation
`scripts/update_feeds.py` (stdlib) pulls YouTube channel RSS (25 educational channels, tagged by line) and 10 education-news RSS/Atom feeds → `data/videos.json`, `data/news.json`. `.github/workflows/auto-refresh.yml` runs daily (05:17 UTC) + on demand: fetch → rebuild → commit → request Pages build.

## Phase 9 — Launch & verification
Push to `WEBWORKSA1/learning-express` (main), enable GitHub Pages (branch `main`, root), run the workflow once, verify every page loads, zero exposed email, internal links resolve, mobile layout, forms post. Then: attach the custom domain (add `CNAME`, update `SITE_URL` in `build/layout.py`), submit sitemap in Search Console, apply to AdSense on the custom domain, confirm the FormSubmit activation email once.
