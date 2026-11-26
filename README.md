# Learning-Express

**The express lane to free learning** — 12 guided Express Lines, original study guides, 8 free study tools, a daily quiz, auto-updated video lessons and education news, plus the free **Program Match** lead funnel.

Static site for GitHub Pages (main branch, root). AdSense publisher `ca-pub-6620975821265271`.

## Structure
- `build/` — Python generator (`build.py`, `layout.py`, `content_lines.py`, `content_guides.py`). Run `python3 build/build.py` to regenerate all HTML, `sitemap.xml`, `robots.txt` and `data/search.json`.
- `scripts/update_feeds.py` — daily fetch of YouTube lessons and education news (sources in `data/sources.json`).
- `.github/workflows/auto-refresh.yml` — runs daily and on demand; commits refreshed data/pages.
- `data/contests.json` — edit contest names/prizes here.
- `assets/` — CSS, JS (core, tools, quiz, match funnel, videos), images.
- `docs/RESEARCH.md` — 39-site competitive research. `docs/BUILD-PROMPT.md` — phase-wise build prompt.

## Custom domain
When the domain is pointed at GitHub Pages: add a `CNAME` file with the domain, set `SITE_URL` in `build/layout.py`, rebuild and push.

## Notices
Learning-Express is independent and not affiliated with EBSCO or "LearningExpress". See `disclaimer.html`.
