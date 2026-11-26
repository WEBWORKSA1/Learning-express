#!/usr/bin/env python3
"""Learning-Express static site generator. Run: python3 build/build.py  (writes HTML to repo root)."""
import json, math, os, sys, datetime, html
sys.path.insert(0, os.path.dirname(__file__))
from layout import page, esc, SITE_URL, honeypot
from content_lines import LINES
from content_guides import GUIDES

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TODAY = datetime.date.today().isoformat()
OUT = {}  # path -> (html, priority)
SEARCH = []

def load(name, default):
    p = os.path.join(ROOT, "data", name)
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

NEWS = load("news.json", {"updated": None, "items": []})
VIDEOS = load("videos.json", {"updated": None, "items": [], "channels": []})
CONTESTS = load("contests.json", {})

def emit(path, html_, prio=0.6, search=None):
    OUT[path] = (html_, prio)
    if search:
        SEARCH.append({"t": search[0], "u": path, "d": search[1], "k": search[2] if len(search) > 2 else ""})

def ext(url):
    return url.startswith("http")

def a(url, label):
    if ext(url):
        return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)} ↗</a>'
    return f'<a href="{esc(url)}">{esc(label)}</a>'

def fmt_date(iso):
    try:
        d = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return d.strftime("%b %d, %Y")
    except Exception:
        return ""

# ---------------------------------------------------------------- components
def line_card(L):
    return f'''<a class="card line-card reveal" href="path-{L["slug"]}.html" style="--c:{L["color"]}">
<span class="line-badge">{L["code"]}</span><h3>{esc(L["name"])}</h3><p>{esc(L["tag"])}</p>
<div class="meta"><span>🚉 {len(L["stations"])} stations</span><span>⏱ ~{L["hours"]} h</span><span>💸 Free</span></div></a>'''

def guide_card(G):
    return f'''<a class="card reveal" href="guide-{G["slug"]}.html"><span class="tag">{esc(G["cat"])} · {G["mins"]} min read</span>
<h3 style="margin-top:10px">{esc(G["title"])}</h3><p>{esc(G["desc"])}</p></a>'''

def news_rows(items, n=None):
    rows = []
    for it in items[: n or len(items)]:
        rows.append(f'''<div class="news-item"><span class="src">{esc(it.get("source",""))}<br><span style="color:var(--muted);font-weight:500">{esc(fmt_date(it.get("date","")))}</span></span>
<div><a href="{esc(it["link"])}" target="_blank" rel="noopener nofollow">{esc(it["title"])}</a><p class="note mb0">{esc(it.get("summary","")[:180])}</p></div></div>''')
    return "".join(rows) or '<p class="note">Fresh headlines load automatically every day.</p>'

def video_cards(items, n=6):
    out = []
    for v in items[:n]:
        thumb = f'https://i.ytimg.com/vi/{v["id"]}/hqdefault.jpg'
        out.append(f'''<div class="card vcard"><div class="vid" role="button" tabindex="0" aria-label="Play: {esc(v["title"])}" data-id="{esc(v["id"])}" data-title="{esc(v["title"])}"><img loading="lazy" src="{thumb}" alt=""><div class="play"><span></span></div></div>
<h3>{esc(v["title"])}</h3><div class="meta"><span>{esc(v.get("channel",""))}</span><span>{esc(fmt_date(v.get("date","")))}</span></div></div>''')
    return "".join(out)

def netmap_svg():
    W, H, cx, cy = 1160, 440, 580, 220
    parts = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Express Lines network map"><title>Learning-Express network map</title>']
    hub = [L for L in LINES if L["slug"] == "study-skills"][0]
    others = [L for L in LINES if L["slug"] != "study-skills"]
    n = len(others)
    for i, L in enumerate(others):
        ang = (i / n) * 2 * math.pi - math.pi / 2
        ex, ey = cx + math.cos(ang) * 360, cy + math.sin(ang) * 180
        mx, my = cx + math.cos(ang) * 150, cy + math.sin(ang) * 70
        parts.append(f'<a href="path-{L["slug"]}.html"><polyline points="{cx},{cy} {mx:.0f},{my:.0f} {ex:.0f},{ey:.0f}" fill="none" stroke="{L["color"]}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" opacity=".92"/>')
        for t in (0.45, 0.72):
            sx, sy = mx + (ex - mx) * t, my + (ey - my) * t
            parts.append(f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="6" fill="var(--surface)" stroke="{L["color"]}" stroke-width="4"/>')
        anchor = "end" if ex < cx - 40 else ("start" if ex > cx + 40 else "middle")
        lx = ex + (-14 if anchor == "end" else 14 if anchor == "start" else 0)
        ly = ey + (5 if anchor != "middle" else (-16 if ey < cy else 26))
        parts.append(f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="11" fill="{L["color"]}"/><text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anchor}" font-family="Inter,sans-serif" font-size="14" font-weight="700" fill="var(--ink)">{esc(L["short"])}</text></a>')
    parts.append(f'<a href="path-study-skills.html"><circle cx="{cx}" cy="{cy}" r="30" fill="{hub["color"]}" stroke="var(--surface)" stroke-width="6"/><text x="{cx}" y="{cy+5}" text-anchor="middle" font-family="Inter,sans-serif" font-size="13" font-weight="800" fill="#fff" style="stroke:none">STDY</text><text x="{cx}" y="{cy+52}" text-anchor="middle" font-family="Inter,sans-serif" font-size="13" font-weight="700" fill="var(--ink)">Study Skills hub</text></a></svg>')
    return "".join(parts)

def nl_strip():
    return f'''<section class="sec"><div class="wrap"><div class="nl reveal">
<div><span class="pill">EXPRESS WEEKLY</span><h2 style="margin-top:12px">5 free lessons worth your time, every Friday.</h2>
<p class="mb0">Hand-picked videos, new Express Lines, contest announcements and the printable 30-Day Planner. Free forever.</p></div>
<div><form data-lx="Newsletter signup" data-ok="You're in! Watch your inbox on Friday. Meanwhile, grab the <a href='planner.html' style='color:inherit'>30-Day Planner</a>.">
<input type="email" name="email" placeholder="you@email.com" required aria-label="Email address">
<input type="hidden" name="list" value="Express Weekly">{honeypot()}
<button class="btn ink" type="submit">Subscribe free</button></form>
<p class="note" style="color:#DDE3FF;margin-top:10px">Join learners from 100+ countries. Unsubscribe anytime.</p></div>
</div></div></section>'''

def match_cta(title="Not sure which program is right for you?", sub="Answer 7 quick questions and get a free, personalised shortlist of courses, certificates, bootcamps or degrees that fit your goal, budget and schedule."):
    return f'''<section class="sec ink"><div class="wrap split" id="matchcta">
<div><span class="eyebrow" style="background:rgba(184,242,74,.14);color:var(--lime)">FREE · 60 SECONDS · NO OBLIGATION</span>
<h2>{esc(title)}</h2><p style="font-size:1.1rem">{esc(sub)}</p>
<div class="badges"><span>✓ Independent</span><span>✓ Free forever</span><span>✓ You choose who contacts you</span></div></div>
<div class="card" style="color:var(--ink)"><h3>What's your main goal?</h3>
<div class="grid" style="gap:10px">
<a class="btn ghost block" href="match.html?goal=career">🚀 Start a new career</a>
<a class="btn ghost block" href="match.html?goal=promotion">📈 Get promoted / upskill</a>
<a class="btn ghost block" href="match.html?goal=degree">🎓 Earn a degree or diploma</a>
<a class="btn ghost block" href="match.html?goal=exam">📝 Pass an exam or certification</a></div></div>
</div></section>'''

# ---------------------------------------------------------------- home
def build_home():
    lines = "".join(line_card(L) for L in LINES)
    guides = "".join(guide_card(G) for G in GUIDES[:3])
    vids = video_cards(VIDEOS.get("items", []), 6)
    opts = "".join(f'<option value="{L["slug"]}">{esc(L["name"].replace(" Line",""))}</option>' for L in LINES)
    body = f'''
<section class="hero"><div class="speed"></div><div class="wrap">
<div>
<span class="eyebrow">🚄 12 FREE LEARNING LINES · NO SIGN-UP NEEDED</span>
<h1>The express lane to <span style="color:var(--brand)">free learning</span>.</h1>
<p class="lead">Pick a destination — a new skill, a better job, an exam — and ride a step-by-step line of the best free lessons, videos and practice on the web. Track every station, test yourself daily and get matched with programs when you're ready to go further.</p>
<div class="hero-cta"><a class="btn signal" href="#finder" style="color:#fff">Find my Express Line</a><a class="btn ghost" href="match.html">Get a free Program Match →</a></div>
<div class="trust"><span>100% free lessons</span><span>Curated from top open-education sources</span><span>Progress saved on your device</span></div>
</div>
<div class="hero-card" id="finder">
<span class="pill">LINE FINDER</span>
<h3 style="margin-top:12px">Where do you want to go?</h3>
<p class="note">Choose a destination and we'll route you to the fastest free line.</p>
<form class="form" id="finderForm" onsubmit="event.preventDefault();location.href='path-'+this.dest.value+'.html'">
<label class="f">I want to…<select name="dest">{opts}</select></label>
<label class="f">Time I can give each week<select name="t"><option>2–4 hours</option><option selected>5–8 hours</option><option>10+ hours</option></select></label>
<button class="btn block" type="submit">Show my route →</button></form>
<div class="search-box" style="margin-top:14px"><input id="siteSearch" type="search" placeholder="Or search lessons, guides, tools…" aria-label="Search the site"><div class="search-res" id="searchRes"></div></div>
</div></div></section>

<section class="sec alt"><div class="wrap"><div class="stats">
<div class="stat"><b>12</b>Express Lines</div><div class="stat"><b>72</b>Guided stations</div><div class="stat"><b>8</b>Free study tools</div><div class="stat"><b>Daily</b>Auto-updated videos &amp; news</div>
</div></div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">THE NETWORK</span><h2>Every line connects through Study Skills.</h2></div><p>Learn how to learn first, then transfer to any line. Click a line to see its stations.</p></div>
<div class="netmap reveal">{netmap_svg()}</div>
</div></section>

<section class="sec alt"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">EXPRESS LINES</span><h2>Choose your destination</h2></div><a class="btn ghost" href="paths.html">All lines</a></div>
<div class="grid g3">{lines}</div></div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">HOW IT WORKS</span><h2>Learn faster in three moves</h2></div></div>
<div class="grid g3">
<div class="card reveal"><span class="line-badge" style="--c:#1F5BFF">1</span><h3>Board a line</h3><p>Each line breaks a goal into 6 stations with time estimates and the best free resources — no more tutorial hopping.</p></div>
<div class="card reveal"><span class="line-badge" style="--c:#FF5A1F">2</span><h3>Practise &amp; test</h3><p>Use flashcards, the focus timer and the Daily Quiz. Active recall and spaced review are built in.</p></div>
<div class="card reveal"><span class="line-badge" style="--c:#14A44D">3</span><h3>Go further</h3><p>Ready for a credential? Program Match gives you an independent shortlist of courses, bootcamps and degrees.</p></div>
</div></div></section>

{match_cta()}

<section class="sec"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">VIDEO EXPRESS</span><h2>Fresh lessons from top educators</h2></div><a class="btn ghost" href="videos.html">Video library</a></div>
<div class="grid g3" id="homeVideos">{vids or '<p class="note">Loading the latest lessons…</p>'}</div></div></section>

<section class="sec alt"><div class="wrap">
<div class="grid g2" style="align-items:center">
<div><span class="eyebrow">DAILY QUIZ</span><h2>Five questions. Two minutes. Every day.</h2><p class="lead">A new mixed quiz unlocks daily — science, math, money, tech and more. Keep your streak alive (you're on day <strong data-streak>1</strong>).</p><a class="btn" href="quiz.html">Take today's quiz</a></div>
<div class="grid g2">
<a class="card" href="tools.html#flash"><h3>🃏 Flashcards</h3><p>Make decks, flip, and track what you know.</p></a>
<a class="card" href="tools.html#timer"><h3>⏱ Focus Timer</h3><p>Pomodoro sprints with auto breaks.</p></a>
<a class="card" href="tools.html#planner"><h3>📅 Review Scheduler</h3><p>Spaced-repetition dates in one click.</p></a>
<a class="card" href="tools.html#gpa"><h3>🎓 GPA Calculator</h3><p>Weighted grades and GPA instantly.</p></a>
</div></div></div></section>

<section class="sec"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">GUIDES</span><h2>Study smarter, not longer</h2></div><a class="btn ghost" href="guides.html">All guides</a></div>
<div class="grid g3">{guides}</div></div></section>

<section class="sec alt"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">LEARNING NEWS · UPDATED DAILY</span><h2>What's new in education</h2></div><a class="btn ghost" href="news.html">All news</a></div>
<div>{news_rows(NEWS.get("items", []), 6)}</div></div></section>

<section class="sec"><div class="wrap"><div class="grid g3">
<a class="card line-card reveal" style="--c:#FF5A1F" href="contests.html"><span class="tag">This month</span><h3 style="margin-top:8px">🏆 Contests &amp; prizes</h3><p>Join the Learning Streak Challenge or the Explain-It-Simply contest and win prizes.</p></a>
<a class="card line-card reveal" style="--c:#14A44D" href="support.html"><span class="tag">Keep it free</span><h3 style="margin-top:8px">💚 Support Learning-Express</h3><p>Your support funds new lines, creators, contests and prizes for learners worldwide.</p></a>
<a class="card line-card reveal" style="--c:#1F5BFF" href="careers.html"><span class="tag">We're hiring</span><h3 style="margin-top:8px">🧑‍🏫 Creators &amp; tutors</h3><p>Writers, video creators, subject experts and ambassadors — join the crew.</p></a>
</div></div></section>

{nl_strip()}

<section class="sec alt"><div class="wrap narrow">
<h2 class="center">Questions, answered</h2>
<details class="faq"><summary>Is Learning-Express really free?</summary><p>Yes. Every line, guide, tool and quiz is free with no account required. We are supported by advertising, optional donations and partners — never by paywalls.</p></details>
<details class="faq"><summary>Do you create the courses?</summary><p>We design the routes, write the guides and build the tools. The lessons we link to come from reputable open-education providers, universities and creators, credited on every station.</p></details>
<details class="faq"><summary>How does Program Match work?</summary><p>You answer seven questions. We suggest program types that fit and, only if you opt in, may introduce you to education partners. You are never obliged to enrol.</p></details>
<details class="faq"><summary>Is my progress saved?</summary><p>Station check-offs, flashcards and streaks are stored privately in your own browser. Clearing browser data resets them.</p></details>
</div></section>
'''
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": "Is Learning-Express really free?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. Every line, guide, tool and quiz is free with no account required."}},
        {"@type": "Question", "name": "How does Program Match work?", "acceptedAnswer": {"@type": "Answer", "text": "Answer seven questions to get a shortlist of program types; partner introductions happen only if you opt in."}}]}
    emit("index.html", page("index.html", "Learning-Express — Free Express Learning Lines, Study Tools & Program Match",
        "Free step-by-step learning lines for AI, coding, data, marketing, finance, languages and more — plus study tools, a daily quiz, curated videos and free program matching.", body, ld=ld, active="index.html", extra_js='<script src="assets/js/videos.js" defer></script>'), 1.0,
        ("Home", "Free Express Lines, tools and program match"))

# ---------------------------------------------------------------- lines
def build_lines():
    cards = "".join(line_card(L) for L in LINES)
    body = f'''<section class="hero" style="padding-bottom:20px"><div class="wrap" style="display:block">
<div class="crumbs"><a href="index.html">Home</a> / Express Lines</div>
<span class="eyebrow">12 LINES · 72 STATIONS</span><h1>Express Lines</h1>
<p class="lead">Each line is a guided route to a real-world outcome. Stations list time estimates and hand-picked free resources. Check stations off as you go — your progress is saved in this browser.</p></div></section>
<section class="sec" style="padding-top:10px"><div class="wrap"><div class="netmap" style="margin-bottom:28px">{netmap_svg()}</div><div class="grid g3">{cards}</div></div></section>
{match_cta()}{nl_strip()}'''
    emit("paths.html", page("paths.html", "Express Lines: 12 Free Step-by-Step Learning Paths", "Browse 12 free learning paths with 72 guided stations — AI, coding, data, marketing, personal finance, languages, business, careers, math, science and health careers.", body), 0.9,
         ("Express Lines", "All 12 free learning paths", "paths roadmap"))
    for i, L in enumerate(LINES):
        sts = []
        for j, (t, h, d, res) in enumerate(L["stations"]):
            key = f'{L["slug"]}-{j}'
            links = "".join(a(u, lab) for lab, u in res)
            sts.append(f'''<li><h3><span class="line-badge" style="min-width:30px;height:30px;font-size:.8rem;margin:0">{j+1}</span>{esc(t)}<span class="time">~{h} h</span></h3>
<p class="mb0">{esc(d)}</p><div class="res">{links}</div>
<label class="chk"><input type="checkbox" data-station="{key}"> Station complete</label></li>''')
        faq = "".join(f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(ans)}</p></details>' for q, ans in L["faq"])
        intro = "".join(f"<p>{esc(p)}</p>" for p in L["intro"])
        nxt = LINES[(i + 1) % len(LINES)]
        yt = "https://www.youtube.com/results?search_query=" + L["yt"].replace(" ", "+")
        body = f'''<section class="hero" style="padding-bottom:24px;--c:{L["color"]}"><div class="wrap" style="display:block">
<div class="crumbs"><a href="index.html">Home</a> / <a href="paths.html">Express Lines</a> / {esc(L["name"])}</div>
<span class="line-badge" style="--c:{L["color"]}">{L["code"]}</span>
<h1>{esc(L["name"])}</h1><p class="lead">{esc(L["tag"])}</p>
<div class="meta" style="font-size:.95rem"><span>🚉 {len(L["stations"])} stations</span><span>⏱ ~{L["hours"]} hours total</span><span>💸 All resources free</span><span>🎯 {esc(L["for"])}</span></div>
</div></section>
<section class="sec" style="padding-top:10px;--c:{L["color"]}"><div class="wrap layout-side">
<article class="article">
{intro}
<div class="callout"><strong>Destination:</strong> {esc(L["outcome"])}</div>
<div class="progress" style="--c:{L["color"]};margin-top:22px"><i data-progress></i></div><p class="note" data-progress-label>0 stations · 0%</p>
<h2>The route</h2>
<ol class="stations" style="--c:{L["color"]}">{"".join(sts)}</ol>
<h2>Video lessons for this line</h2>
<p>New lessons from our curated channels appear here automatically each day.</p>
<div class="grid g2" data-line-videos="{L["cat"]}"></div>
<p style="margin-top:14px"><a href="{esc(yt)}" target="_blank" rel="noopener">Browse more {esc(L["name"].replace(" Line",""))} videos on YouTube ↗</a></p>
<h2>FAQ</h2>{faq}
</article>
<aside class="sticky">
<div class="card" style="border-top:6px solid {L["color"]}"><h3>Want a credential?</h3><p>Compare certificates, bootcamps and degrees for {esc(L["name"].replace(" Line","").lower())} — free and independent.</p>
<a class="btn signal block" href="match.html?field={L["cat"]}" style="color:#fff">Get my Program Match</a></div>
<div class="card" style="margin-top:16px"><h3>Daily review</h3><p class="note">Turn each station into flashcards and review them tomorrow.</p><a class="btn ghost block" href="tools.html#flash">Open flashcards</a></div>
<div class="card" style="margin-top:16px"><span class="tag">Next line</span><h3 style="margin-top:6px"><a href="path-{nxt["slug"]}.html">{esc(nxt["name"])} →</a></h3><p class="note mb0">{esc(nxt["tag"])}</p></div>
</aside></div></section>
{nl_strip()}'''
        ld = {"@context": "https://schema.org", "@type": "Course", "name": L["name"], "description": L["tag"],
              "provider": {"@type": "Organization", "name": "Learning-Express", "sameAs": SITE_URL},
              "isAccessibleForFree": True, "timeRequired": f'PT{L["hours"]}H',
              "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "online", "courseWorkload": f'PT{L["hours"]}H'},
              "offers": {"@type": "Offer", "price": 0, "priceCurrency": "USD", "category": "Free"}}
        emit(f'path-{L["slug"]}.html', page(f'path-{L["slug"]}.html', f'{L["name"]}: Free Step-by-Step Roadmap', f'{L["tag"]} A free {len(L["stations"])}-station roadmap (~{L["hours"]} hours) with the best free resources.', body, active="paths.html", ld=ld, extra_js='<script src="assets/js/videos.js" defer></script>'), 0.8,
             (L["name"], L["tag"], " ".join(s[0] for s in L["stations"])))

# ---------------------------------------------------------------- guides
def build_guides():
    cards = "".join(guide_card(G) for G in GUIDES)
    body = f'''<section class="hero" style="padding-bottom:20px"><div class="wrap" style="display:block"><div class="crumbs"><a href="index.html">Home</a> / Guides</div>
<span class="eyebrow">ORIGINAL GUIDES</span><h1>Study Guides</h1><p class="lead">Evidence-based techniques and career playbooks, written in plain language. Read one, apply it today.</p></div></section>
<section class="sec" style="padding-top:10px"><div class="wrap"><div class="grid g3">{cards}</div></div></section>{nl_strip()}'''
    emit("guides.html", page("guides.html", "Study Guides: Learning Science & Career Playbooks", "Free guides on active recall, spaced repetition, the Feynman technique, focus, free certificates, choosing online programs and switching careers.", body), 0.8, ("Guides", "All study guides"))
    for i, G in enumerate(GUIDES):
        rel = [GUIDES[(i + k) % len(GUIDES)] for k in (1, 2, 3)]
        relh = "".join(f'<li><a href="guide-{r["slug"]}.html">{esc(r["title"])}</a></li>' for r in rel)
        body = f'''<section class="sec" style="padding-top:40px"><div class="wrap layout-side">
<article class="article"><div class="crumbs"><a href="index.html">Home</a> / <a href="guides.html">Guides</a> / {esc(G["cat"])}</div>
<span class="tag" style="font:700 .75rem var(--f-mono);color:var(--signal)">{esc(G["cat"]).upper()} · {G["mins"]} MIN READ · UPDATED {datetime.date.today().strftime("%b %Y").upper()}</span>
<h1 style="font-size:clamp(2rem,4vw,3rem);margin-top:10px">{esc(G["title"])}</h1>
<p class="lead">{esc(G["desc"])}</p>
{G["body"]}
<hr style="border:0;border-top:1px solid var(--line);margin:30px 0">
<p class="note">Written by the Learning-Express editorial team. This guide is for general education and is not professional, medical, legal or financial advice.</p>
</article>
<aside class="sticky">
<div class="card"><h3>Keep reading</h3><ul style="padding-left:1.1em;margin:0">{relh}</ul></div>
<div class="card" style="margin-top:16px;border-top:6px solid var(--signal)"><h3>Free Program Match</h3><p class="note">Get an independent shortlist of programs for your goal in 60 seconds.</p><a class="btn signal block" href="match.html" style="color:#fff">Start now</a></div>
<div class="card" style="margin-top:16px"><h3>Express Weekly</h3><form class="form" data-lx="Newsletter signup (guide sidebar)"><input type="email" name="email" placeholder="you@email.com" required aria-label="Email"><input type="hidden" name="list" value="Express Weekly">{honeypot()}<button class="btn block" type="submit">Subscribe</button></form></div>
</aside></div></section>'''
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": G["title"], "description": G["desc"],
              "author": {"@type": "Organization", "name": "Learning-Express Editorial"}, "publisher": {"@type": "Organization", "name": "Learning-Express"},
              "dateModified": TODAY, "mainEntityOfPage": f'{SITE_URL}/guide-{G["slug"]}.html'}
        emit(f'guide-{G["slug"]}.html', page(f'guide-{G["slug"]}.html', G["title"], G["desc"], body, active="guides.html", ld=ld, og_type="article"), 0.7, (G["title"], G["desc"], G["cat"]))

# ---------------------------------------------------------------- videos & news
def build_videos():
    cats = [("all", "All"), ("ai", "AI"), ("web", "Coding"), ("data", "Data"), ("mkt", "Marketing"), ("fin", "Finance"), ("lang", "Languages"), ("biz", "Business"), ("job", "Careers"), ("study", "Study skills"), ("math", "Math"), ("sci", "Science"), ("care", "Health careers")]
    chips = "".join(f'<button class="chip" data-cat="{c}" aria-pressed="{"true" if c=="all" else "false"}">{t}</button>' for c, t in cats)
    upd = VIDEOS.get("updated")
    body = f'''<section class="hero" style="padding-bottom:16px"><div class="wrap" style="display:block"><div class="crumbs"><a href="index.html">Home</a> / Videos</div>
<span class="eyebrow">AUTO-UPDATED DAILY</span><h1>Video Express Library</h1>
<p class="lead">The newest lessons from respected educational channels, sorted by line. Videos play through YouTube's privacy-enhanced embed.</p>
<p class="note">{"Last refreshed " + esc(fmt_date(upd)) if upd else "Refreshes automatically every day."}</p></div></section>
<section class="sec" style="padding-top:10px"><div class="wrap">
<div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-bottom:12px"><input id="vq" type="search" placeholder="Search videos…" style="max-width:320px" aria-label="Search videos"></div>
<div class="chips" id="vchips">{chips}</div>
<div class="grid g3" id="vgrid">{video_cards(VIDEOS.get("items", []), 12)}</div>
<p class="center" style="margin-top:24px"><button class="btn ghost" id="vmore">Load more</button></p>
<h2 style="margin-top:50px">Featured channels</h2><div class="grid g4" id="vchan"></div>
</div></section>{match_cta()}'''
    emit("videos.html", page("videos.html", "Free Video Lessons Library (Updated Daily)", "Watch the latest free lessons from top educational YouTube channels — AI, coding, math, science, finance, languages and careers — sorted by learning line.", body, extra_js='<script src="assets/js/videos.js" defer></script>'), 0.8, ("Video Library", "Latest free video lessons", "youtube"))

def build_news():
    items = NEWS.get("items", [])
    srcs = sorted({i.get("source", "") for i in items if i.get("source")})
    chips = '<button class="chip" data-src="all" aria-pressed="true">All sources</button>' + "".join(f'<button class="chip" data-src="{esc(s)}" aria-pressed="false">{esc(s)}</button>' for s in srcs)
    rows = []
    for it in items:
        rows.append(f'<div class="news-item" data-src="{esc(it.get("source",""))}"><span class="src">{esc(it.get("source",""))}<br><span style="color:var(--muted);font-weight:500">{esc(fmt_date(it.get("date","")))}</span></span><div><a href="{esc(it["link"])}" target="_blank" rel="noopener nofollow">{esc(it["title"])}</a><p class="note mb0">{esc(it.get("summary","")[:220])}</p></div></div>')
    upd = NEWS.get("updated")
    body = f'''<section class="hero" style="padding-bottom:16px"><div class="wrap" style="display:block"><div class="crumbs"><a href="index.html">Home</a> / News</div>
<span class="eyebrow">UPDATED EVERY DAY</span><h1>Learning News</h1><p class="lead">Headlines on education, online learning, edtech and careers from trusted publications. Links open the original source.</p>
<p class="note">{"Last refreshed " + esc(fmt_date(upd)) if upd else "Refreshes automatically every day."}</p></div></section>
<section class="sec" style="padding-top:10px"><div class="wrap layout-side"><div><div class="chips" id="nchips">{chips}</div><div id="nlist">{"".join(rows) or '<p class="note">Headlines are being gathered — check back shortly.</p>'}</div></div>
<aside class="sticky"><div class="card"><h3>Get the weekly digest</h3><p class="note">The five headlines that matter, plus free lessons.</p><form class="form" data-lx="Newsletter signup (news)"><input type="email" name="email" placeholder="you@email.com" required aria-label="Email"><input type="hidden" name="list" value="Express Weekly">{honeypot()}<button class="btn block" type="submit">Subscribe</button></form></div>
<div class="card" style="margin-top:16px"><h3>Have education news?</h3><p class="note">Schools, edtech founders and researchers: send us your story.</p><a class="btn ghost block" href="contact.html?topic=press">Send a tip</a></div></aside></div></section>
<script>document.addEventListener("click",function(e){{var b=e.target.closest("#nchips .chip");if(!b)return;document.querySelectorAll("#nchips .chip").forEach(function(c){{c.setAttribute("aria-pressed",c===b?"true":"false")}});var s=b.getAttribute("data-src");document.querySelectorAll("#nlist .news-item").forEach(function(r){{r.style.display=(s==="all"||r.getAttribute("data-src")===s)?"":"none"}})}});</script>'''
    emit("news.html", page("news.html", "Learning News: Education & Online Learning Headlines", "Daily-updated headlines on education, online learning, edtech, skills and careers from trusted sources.", body), 0.7, ("Learning News", "Daily education headlines"))

# ---------------------------------------------------------------- tools, quiz, planner
def build_tools():
    body = f'''<section class="hero" style="padding-bottom:16px"><div class="wrap" style="display:block"><div class="crumbs"><a href="index.html">Home</a> / Study Tools</div>
<span class="eyebrow">8 FREE TOOLS · NO SIGN-UP</span><h1>Study Tools</h1><p class="lead">Everything runs in your browser and saves privately on your device.</p></div></section>
<section class="sec" style="padding-top:10px"><div class="wrap">
<div class="tool-tabs chips" role="tablist">
<button class="chip" data-tool="flash" aria-pressed="true">🃏 Flashcards</button>
<button class="chip" data-tool="timer" aria-pressed="false">⏱ Focus Timer</button>
<button class="chip" data-tool="planner" aria-pressed="false">📅 Review Scheduler</button>
<button class="chip" data-tool="gpa" aria-pressed="false">🎓 GPA Calculator</button>
<button class="chip" data-tool="grade" aria-pressed="false">🧮 Final Grade Needed</button>
<button class="chip" data-tool="reading" aria-pressed="false">📖 Reading Speed</button>
<button class="chip" data-tool="typing" aria-pressed="false">⌨️ Typing Speed</button>
<button class="chip" data-tool="hours" aria-pressed="false">⏳ Goal Hours</button>
</div>

<div class="tool on" id="t-flash"><div class="grid g2">
<div class="card"><h2 style="font-size:1.5rem">Your deck</h2><p class="note">One card per line: <span class="kbd">question :: answer</span></p>
<textarea id="fcInput" rows="8" placeholder="Capital of Canada :: Ottawa&#10;H2O :: Water&#10;Mitochondria :: Powerhouse of the cell"></textarea>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px"><button class="btn sm" id="fcLoad">Load deck</button><button class="btn sm ghost" id="fcSample">Sample deck</button><button class="btn sm ghost" id="fcShuffle">Shuffle</button></div></div>
<div><div class="flash" id="fcCard" tabindex="0" aria-live="polite"><div class="flash-in"><div class="flash-face" id="fcFront">Load a deck to begin</div><div class="flash-face back" id="fcBack">Answer</div></div></div>
<div style="display:flex;gap:8px;justify-content:center;margin-top:14px;flex-wrap:wrap"><button class="btn sm ghost" id="fcAgain">✗ Still learning</button><button class="btn sm" id="fcKnow">✓ I know it</button></div>
<p class="center note" id="fcStat">Click the card to flip · Space = flip</p></div></div></div>

<div class="tool" id="t-timer"><div class="card center" style="max-width:560px;margin:0 auto">
<div class="chips" style="justify-content:center"><button class="chip" data-mins="25" aria-pressed="true">Focus 25</button><button class="chip" data-mins="50" aria-pressed="false">Deep 50</button><button class="chip" data-mins="5" aria-pressed="false">Break 5</button><button class="chip" data-mins="15" aria-pressed="false">Long break 15</button></div>
<div class="timer" id="tmDisplay">25:00</div><p class="note" id="tmLabel">Focus sprint</p>
<div style="display:flex;gap:10px;justify-content:center"><button class="btn" id="tmStart">Start</button><button class="btn ghost" id="tmReset">Reset</button></div>
<p class="note" style="margin-top:14px">Sprints completed today: <strong id="tmCount">0</strong></p></div></div>

<div class="tool" id="t-planner"><div class="card" style="max-width:700px">
<h2 style="font-size:1.5rem">Spaced-review scheduler</h2><p>Enter what you studied and when. We'll calculate review dates at 1, 3, 7, 14 and 30 days.</p>
<div class="form"><div class="row"><label class="f">Topic<input id="spTopic" placeholder="e.g., SQL joins"></label><label class="f">Studied on<input type="date" id="spDate"></label></div>
<button class="btn" id="spGo">Calculate review dates</button></div><div id="spOut" style="margin-top:16px"></div></div></div>

<div class="tool" id="t-gpa"><div class="card" style="max-width:760px">
<h2 style="font-size:1.5rem">GPA calculator (4.0 scale)</h2>
<table class="t" id="gpaTable"><thead><tr><th>Course</th><th>Credits</th><th>Grade</th><th></th></tr></thead><tbody></tbody></table>
<div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap"><button class="btn sm ghost" id="gpaAdd">+ Add course</button></div>
<p style="font-size:1.3rem;margin-top:16px">GPA: <strong id="gpaOut">0.00</strong> <span class="note" id="gpaCred"></span></p></div></div>

<div class="tool" id="t-grade"><div class="card" style="max-width:640px">
<h2 style="font-size:1.5rem">What do I need on the final?</h2>
<div class="form"><div class="row"><label class="f">Current grade (%)<input type="number" id="fgCur" value="82" min="0" max="100"></label><label class="f">Desired course grade (%)<input type="number" id="fgWant" value="85" min="0" max="100"></label></div>
<label class="f">Final exam weight (%)<input type="number" id="fgW" value="30" min="1" max="100"></label></div>
<p style="font-size:1.25rem;margin-top:14px" id="fgOut"></p></div></div>

<div class="tool" id="t-reading"><div class="card" style="max-width:760px">
<h2 style="font-size:1.5rem">Reading speed test</h2><p>Press start, read the passage at a normal pace, then press done.</p>
<div class="typing-text" id="rdText" style="font-family:var(--f-body);display:none"></div>
<div style="display:flex;gap:10px;margin-top:12px"><button class="btn" id="rdStart">Start reading</button><button class="btn ghost" id="rdDone" disabled>Done</button></div>
<p style="font-size:1.2rem;margin-top:14px" id="rdOut"></p></div></div>

<div class="tool" id="t-typing"><div class="card" style="max-width:820px">
<h2 style="font-size:1.5rem">Typing speed test (60 seconds)</h2>
<div class="typing-text" id="tyText"></div><textarea id="tyIn" rows="3" placeholder="Start typing to begin the timer…" style="margin-top:12px"></textarea>
<p style="margin-top:10px"><strong id="tyTime">60</strong>s · <strong id="tyWpm">0</strong> WPM · <strong id="tyAcc">100</strong>% accuracy <button class="btn sm ghost" id="tyReset" style="margin-left:8px">Restart</button></p></div></div>

<div class="tool" id="t-hours"><div class="card" style="max-width:640px">
<h2 style="font-size:1.5rem">Goal-hours calculator</h2><p>How long until you reach your goal?</p>
<div class="form"><div class="row"><label class="f">Hours needed<input type="number" id="ghNeed" value="60"></label><label class="f">Hours per week<input type="number" id="ghWeek" value="5"></label></div></div>
<p style="font-size:1.2rem;margin-top:14px" id="ghOut"></p>
<p class="note">Tip: every Express Line shows its estimated hours. <a href="paths.html">Pick one</a>.</p></div></div>
</div></section>{nl_strip()}'''
    emit("tools.html", page("tools.html", "Free Study Tools: Flashcards, Pomodoro Timer, GPA & More", "Free online study tools: flashcard maker, Pomodoro focus timer, spaced-repetition scheduler, GPA calculator, final grade calculator, reading and typing speed tests.", body, extra_js='<script src="assets/js/tools.js" defer></script>'), 0.8,
         ("Study Tools", "Flashcards, timer, GPA calculator and more", "pomodoro gpa flashcards typing reading"))

def build_quiz():
    body = '''<section class="hero" style="padding-bottom:16px"><div class="wrap" style="display:block"><div class="crumbs"><a href="index.html">Home</a> / Daily Quiz</div>
<span class="eyebrow">NEW EVERY DAY</span><h1>The Daily Express Quiz</h1><p class="lead">Five mixed questions, refreshed every day at midnight. Retrieval practice in two minutes.</p></div></section>
<section class="sec" style="padding-top:10px"><div class="wrap layout-side">
<div class="card" id="quizBox" style="padding:28px"><p class="note">Loading today's quiz…</p></div>
<aside class="sticky"><div class="card"><h3>Your stats</h3><p>Streak: <strong data-streak>1</strong> day(s)</p><p>Best daily score: <strong id="qBest">–</strong></p><p class="mb0">Quizzes completed: <strong id="qDone">0</strong></p></div>
<div class="card" style="margin-top:16px"><h3>Practice by topic</h3><div class="chips" id="qTopics"></div></div>
<div class="card" style="margin-top:16px;border-top:6px solid var(--signal)"><h3>Monthly contest</h3><p class="note">Keep a 30-day quiz streak to enter the Learning Streak Challenge.</p><a class="btn ghost block" href="contests.html">See prizes</a></div></aside>
</div></section>'''
    emit("quiz.html", page("quiz.html", "Daily Quiz: 5 Free Trivia & Knowledge Questions Every Day", "A free daily five-question quiz on science, math, money, technology, language and study skills — practise retrieval and keep your streak.", body, extra_js='<script src="assets/js/quiz.js" defer></script>'), 0.8, ("Daily Quiz", "5 questions every day", "trivia quiz"))

def build_planner():
    days = []
    focus = ["Set your finish line", "Deconstruct the skill", "First practice session", "Active recall day", "Practice + feedback", "Mini project", "Weekly review",
             "New station", "Flashcards & spacing", "Teach it (Feynman)", "Practice under time", "Fix weak spots", "Mini project", "Weekly review",
             "New station", "Mixed practice", "Ask for feedback", "Recall without notes", "Apply to a real task", "Mini project", "Weekly review",
             "New station", "Mock test", "Analyse mistakes", "Spaced review", "Build portfolio piece", "Share your work", "Weekly review", "Final test vs. finish line", "Celebrate & choose next line"]
    for i, f in enumerate(focus, 1):
        rev = [d for d in (1, 3, 7, 14) if i - d >= 1]
        revtxt = ", ".join(f"Day {i-d}" for d in rev) or "—"
        days.append(f'<tr><td><strong>Day {i}</strong></td><td>{esc(f)}</td><td>{revtxt}</td><td style="width:90px">☐ 25m ☐ 50m</td><td style="width:40px">☐</td></tr>')
    body = f'''<section class="sec"><div class="wrap narrow">
<div class="crumbs no-print"><a href="index.html">Home</a> / 30-Day Planner</div>
<span class="pill">PRINTABLE</span><h1 style="margin-top:12px">30-Day Express Study Planner</h1>
<p class="lead">One focus per day, with spaced reviews scheduled for you. Print it, pin it, tick it.</p>
<p class="no-print"><button class="btn" onclick="window.print()">🖨 Print / save as PDF</button> <a class="btn ghost" href="tools.html#timer">Open focus timer</a></p>
<div class="card"><p><strong>My finish line:</strong> ______________________________________________ &nbsp; <strong>By:</strong> ___________</p>
<table class="t"><thead><tr><th>Day</th><th>Focus</th><th>Review topics from</th><th>Sprints</th><th>Done</th></tr></thead><tbody>{"".join(days)}</tbody></table></div>
<p class="note" style="margin-top:16px">Based on our guides to <a href="guide-spaced-repetition.html">spaced repetition</a> and <a href="guide-study-plan.html">weekly planning</a>.</p></div></section>'''
    emit("planner.html", page("planner.html", "Free Printable 30-Day Study Planner", "Print a free 30-day study planner with daily focus prompts and spaced-repetition review days built in.", body), 0.6, ("30-Day Planner", "Printable study planner"))

# ---------------------------------------------------------------- lead gen: program match
def build_match():
    body = f'''<section class="hero" style="padding:46px 0 30px"><div class="wrap">
<div><span class="eyebrow">FREE PROGRAM MATCH · 60 SECONDS</span>
<h1 style="font-size:clamp(2rem,4.4vw,3.3rem)">Find the right course, certificate, bootcamp or degree — without the sales calls.</h1>
<p class="lead">Tell us your goal, budget and schedule. We'll send an independent shortlist of program types and free starter lessons — and, only if you choose, introduce you to vetted education partners.</p>
<div class="badges"><span>🔒 Your data is never sold</span><span>✓ 100% free</span><span>✓ No obligation</span><span>✓ Unsubscribe anytime</span></div>
<div class="grid g3" style="margin-top:24px">
<div class="stat"><b>7</b>quick questions</div><div class="stat"><b>12</b>fields covered</div><div class="stat"><b>$0</b>cost to you</div></div>
</div>
<div class="funnel" id="funnel">
<div class="funnel-top"><span class="note" id="fStepLbl">Step 1 of 7</span><div class="progress"><i id="fBar" style="width:14%"></i></div></div>
<div class="funnel-body">
<div class="step on" data-step="1" data-key="goal"><h3>What's your main goal?</h3><div class="opts">
<button class="opt" data-v="career"><span class="em">🚀</span>Start a new career</button><button class="opt" data-v="promotion"><span class="em">📈</span>Upskill or get promoted</button>
<button class="opt" data-v="degree"><span class="em">🎓</span>Earn a degree or diploma</button><button class="opt" data-v="exam"><span class="em">📝</span>Pass an exam or certification</button>
<button class="opt" data-v="business"><span class="em">💼</span>Skills for my business</button><button class="opt" data-v="child"><span class="em">🧒</span>Help my child learn</button></div></div>
<div class="step" data-step="2" data-key="field"><h3>Which field interests you most?</h3><div class="opts">
<button class="opt" data-v="web"><span class="em">💻</span>Tech &amp; coding</button><button class="opt" data-v="ai"><span class="em">🤖</span>AI &amp; data</button>
<button class="opt" data-v="care"><span class="em">🩺</span>Healthcare</button><button class="opt" data-v="biz"><span class="em">📊</span>Business &amp; management</button>
<button class="opt" data-v="mkt"><span class="em">📣</span>Marketing &amp; design</button><button class="opt" data-v="fin"><span class="em">💰</span>Finance &amp; accounting</button>
<button class="opt" data-v="edu"><span class="em">🍎</span>Education &amp; teaching</button><button class="opt" data-v="trades"><span class="em">🔧</span>Skilled trades</button>
<button class="opt" data-v="lang"><span class="em">🗣</span>Languages / ESL</button><button class="opt" data-v="unsure"><span class="em">🤔</span>Not sure yet</button></div></div>
<div class="step" data-step="3" data-key="level"><h3>Highest education completed?</h3><div class="opts">
<button class="opt" data-v="highschool">High school / GED</button><button class="opt" data-v="somecollege">Some college</button>
<button class="opt" data-v="diploma">College diploma / associate</button><button class="opt" data-v="bachelor">Bachelor's degree</button>
<button class="opt" data-v="master">Master's or higher</button><button class="opt" data-v="other">Other / outside North America</button></div></div>
<div class="step" data-step="4" data-key="format"><h3>How do you prefer to learn?</h3><div class="opts">
<button class="opt" data-v="self">🕐 Online, self-paced</button><button class="opt" data-v="live">🎥 Online, live classes</button>
<button class="opt" data-v="hybrid">🏫 In-person or hybrid</button><button class="opt" data-v="any">🤷 No preference</button></div></div>
<div class="step" data-step="5" data-key="budget"><h3>What budget are you considering?</h3><div class="opts">
<button class="opt" data-v="free">Free only</button><button class="opt" data-v="lt1k">Under $1,000</button>
<button class="opt" data-v="1-5k">$1,000 – $5,000</button><button class="opt" data-v="5-15k">$5,000 – $15,000</button>
<button class="opt" data-v="15k+">$15,000+</button><button class="opt" data-v="aid">I need financial aid / funding</button></div></div>
<div class="step" data-step="6" data-key="timeline"><h3>When would you like to start?</h3><div class="opts">
<button class="opt" data-v="now">⚡ Within 30 days</button><button class="opt" data-v="1-3m">1–3 months</button>
<button class="opt" data-v="3-6m">3–6 months</button><button class="opt" data-v="research">Just researching</button></div></div>
<div class="step" data-step="7"><h3>Where should we send your shortlist?</h3>
<p class="note" id="fPreview"></p>
<form class="form" id="fForm">
<div class="row"><label class="f">First name<input name="first_name" autocomplete="given-name" required></label><label class="f">Last name<input name="last_name" autocomplete="family-name"></label></div>
<div class="row"><label class="f">Email<input type="email" name="email" autocomplete="email" required></label><label class="f">Phone (optional, for faster advice)<input type="tel" name="phone" autocomplete="tel"></label></div>
<div class="row"><label class="f">Country<select name="country" required><option value="">Choose…</option><option>United States</option><option>Canada</option><option>United Kingdom</option><option>India</option><option>Australia</option><option>Other</option></select></label><label class="f">ZIP / postal code<input name="postal" autocomplete="postal-code"></label></div>
<label class="chk" style="display:flex;gap:10px;align-items:flex-start;font-size:.88rem"><input type="checkbox" name="partner_consent" value="yes" style="width:auto;margin-top:4px"> Yes, I'd like Learning-Express to share my answers with up to 3 relevant education partners so they can contact me about programs (optional).</label>
{honeypot()}
<button class="btn signal block" type="submit">Get my free shortlist →</button>
<p class="note">By submitting you agree to our <a href="privacy.html">Privacy Policy</a> and <a href="terms.html">Terms</a>. We never sell your data.</p>
</form>
<div id="fResult"></div></div>
<div class="funnel-nav"><button class="btn ghost sm" id="fBack" style="visibility:hidden">← Back</button><span class="note">🔒 Secure &amp; private</span></div>
</div></div>
</div></section>
<section class="sec alt"><div class="wrap"><div class="grid g3">
<div class="card"><h3>Independent</h3><p>We recommend program <em>types</em> based on your answers first. Partner introductions happen only with your explicit consent.</p></div>
<div class="card"><h3>Evidence-based</h3><p>Our shortlist follows the checklist in our guide to <a href="guide-choose-online-program.html">choosing an online program</a>: accreditation, outcomes, total cost.</p></div>
<div class="card"><h3>Start free</h3><p>Every shortlist includes a free Express Line, so you can test a field before paying for anything.</p></div>
</div></div></section>
<section class="sec"><div class="wrap narrow"><h2>Program Match FAQ</h2>
<details class="faq"><summary>Why is Program Match free?</summary><p>Some education partners pay a referral fee when a learner who opted in chooses to contact or enrol with them. This never changes the free resources we recommend.</p></details>
<details class="faq"><summary>Will I get spam calls?</summary><p>No. Leave the partner box unticked and you'll hear only from us. If you tick it, at most three relevant partners may reach out, and you can opt out anytime.</p></details>
<details class="faq"><summary>Do you cover Canada, the UK and India?</summary><p>Yes. Online program options are global; we tailor suggestions to your country.</p></details>
</div></section>'''
    emit("match.html", page("match.html", "Free Program Match: Find the Right Course, Bootcamp or Degree", "Answer 7 quick questions and get a free, independent shortlist of online courses, certificates, bootcamps and degrees that fit your goal, budget and schedule.", body, extra_js='<script src="assets/js/match.js" defer></script>'), 0.9,
         ("Program Match", "Free shortlist of courses, bootcamps and degrees", "degree bootcamp certificate online college"))

# ---------------------------------------------------------------- monetisation & community pages
def build_support():
    body = f'''<section class="hero" style="padding-bottom:24px"><div class="wrap" style="display:block"><div class="crumbs"><a href="index.html">Home</a> / Support</div>
<span class="eyebrow">💚 KEEP LEARNING FREE</span><h1>Support Learning-Express</h1>
<p class="lead">Every line, tool and guide here is free. Your support pays for servers, new content, talented creators, promotion to reach more learners, and the prizes in our monthly contests.</p></div></section>
<section class="sec" style="padding-top:10px"><div class="wrap layout-side"><div>
<div class="card"><h2 style="font-size:1.6rem">Choose your support</h2>
<div class="chips" id="freq"><button class="chip" data-f="One-time" aria-pressed="true">One-time</button><button class="chip" data-f="Monthly" aria-pressed="false">Monthly</button></div>
<div class="tiers" id="tiers">
<button class="tier" data-amt="5" aria-pressed="false"><strong>$5</strong>☕ Coffee for the crew</button>
<button class="tier" data-amt="25" aria-pressed="true"><strong>$25</strong>📚 Funds one new station</button>
<button class="tier" data-amt="100" aria-pressed="false"><strong>$100</strong>🏆 Sponsors a contest prize</button>
<button class="tier" data-amt="500" aria-pressed="false"><strong>$500</strong>🚄 Builds a whole new line</button></div>
<form class="form" data-lx="Donation pledge" data-ok="Thank you for supporting free learning! We'll email you a secure payment link (card, PayPal or bank transfer) within 1 business day." style="margin-top:20px" id="donForm">
<div class="row"><label class="f">Amount (USD)<input type="number" name="amount" id="donAmt" value="25" min="1" required></label>
<label class="f">Use my support for<select name="purpose"><option>Where it's needed most</option><option>Ongoing operations</option><option>Promotions &amp; marketing</option><option>Hiring creators &amp; talent</option><option>Contests &amp; prizes</option><option>Scholarships for learners</option></select></label></div>
<div class="row"><label class="f">Name<input name="name" required autocomplete="name"></label><label class="f">Email<input type="email" name="email" required autocomplete="email"></label></div>
<input type="hidden" name="frequency" id="donFreq" value="One-time">
<label class="f">Message (optional)<textarea name="message" rows="3" placeholder="Why you support free learning…"></textarea></label>
<label class="chk" style="display:flex;gap:8px;font-size:.9rem"><input type="checkbox" name="public_thanks" value="yes" style="width:auto"> Thank me publicly on the supporters wall</label>
{honeypot()}
<button class="btn signal block" type="submit">Pledge my support</button>
<p class="note">Pledges are confirmed with a secure payment link by email. Learning-Express is not a registered charity; contributions are not tax-deductible.</p></form></div>
<h2 style="margin-top:40px">Where your support goes</h2>
<div class="card alloc">
<div><span>Ongoing operations</span><div class="progress"><i style="width:30%;background:#1F5BFF"></i></div><b>30%</b></div>
<div><span>Hiring creators &amp; talent</span><div class="progress"><i style="width:25%;background:#6D28D9"></i></div><b>25%</b></div>
<div><span>Contests &amp; prizes</span><div class="progress"><i style="width:25%;background:#FF5A1F"></i></div><b>25%</b></div>
<div><span>Promotion &amp; marketing</span><div class="progress"><i style="width:20%;background:#14A44D"></i></div><b>20%</b></div></div>
<h2 style="margin-top:40px">Other ways to help</h2>
<div class="grid g3"><div class="card"><h3>Share a line</h3><p>Send an Express Line to one friend who is stuck. Word of mouth is our biggest growth channel.</p><button class="btn sm ghost" onclick="navigator.share?navigator.share({{title:'Learning-Express',url:location.origin+location.pathname.replace('support.html','')}}):navigator.clipboard.writeText(location.href.replace('support.html',''));LX.toast('Link ready to share!')">Share</button></div>
<div class="card"><h3>Volunteer</h3><p>Review stations, translate guides or moderate contests.</p><a class="btn sm ghost" href="careers.html">Join the crew</a></div>
<div class="card"><h3>Sponsor</h3><p>Brands and schools can sponsor a line, a contest or a scholarship.</p><a class="btn sm ghost" href="partners.html">Sponsorship packages</a></div></div>
</div>
<aside class="sticky"><div class="card"><h3>Why support?</h3><ul style="padding-left:1.1em"><li>No paywalls, ever</li><li>New lines added as funding allows</li><li>Prizes for learners in every contest</li><li>Paid, fairly-treated creators</li></ul></div>
<div class="card" style="margin-top:16px"><h3>Corporate &amp; partnership inquiries</h3><p class="note">Sponsorship, advertising or acquiring this website/domain.</p><a class="btn ghost block" data-contact href="#">Contact the owner</a></div></aside>
</div></section>'''
    js = '''<script>document.addEventListener("DOMContentLoaded",function(){var amt=document.getElementById("donAmt");document.querySelectorAll("#tiers .tier").forEach(function(t){t.addEventListener("click",function(){document.querySelectorAll("#tiers .tier").forEach(function(x){x.setAttribute("aria-pressed",x===t?"true":"false")});amt.value=t.getAttribute("data-amt")})});document.querySelectorAll("#freq .chip").forEach(function(c){c.addEventListener("click",function(){document.querySelectorAll("#freq .chip").forEach(function(x){x.setAttribute("aria-pressed",x===c?"true":"false")});document.getElementById("donFreq").value=c.getAttribute("data-f")})})});</script>'''
    emit("support.html", page("support.html", "Support Free Learning: Donate or Sponsor", "Support Learning-Express to keep learning free: fund operations, new content, creators, promotion, contests and prizes.", body, extra_js=js), 0.6, ("Support Us", "Donate and keep learning free", "donate"))

def build_contests():
    contests = CONTESTS.get("contests", [])
    cards = []
    for c in contests:
        prizes = "".join(f"<li>{esc(p)}</li>" for p in c.get("prizes", []))
        cards.append(f'''<div class="card line-card" style="--c:{esc(c.get("color","#FF5A1F"))}"><span class="pill">{esc(c.get("status","OPEN"))}</span><h3 style="margin-top:10px">{esc(c["name"])}</h3>
<p>{esc(c["about"])}</p><p class="note"><strong>How to enter:</strong> {esc(c["how"])}</p><h4 style="font-size:1rem;margin:10px 0 4px">Prizes</h4><ul style="padding-left:1.1em;margin:0 0 10px">{prizes}</ul>
<p class="note mb0"><strong>Judging:</strong> {esc(c["judging"])}</p></div>''')
    opts = "".join(f'<option>{esc(c["name"])}</option>' for c in contests)
    body = f'''<section class="hero" style="padding-bottom:24px"><div class="wrap" style="display:block"><div class="crumbs"><a href="index.html">Home</a> / Contests</div>
<span class="eyebrow">🏆 <span id="cMonth">THIS MONTH</span></span><h1>Contests &amp; Prizes</h1>
<p class="lead">Learn something, show it, win something. New contests every month — free to enter, judged on skill and effort.</p>
<p><strong>Entries close:</strong> <span id="cClose">the last day of this month</span> · <strong>Winners announced:</strong> within 14 days</p></div></section>
<section class="sec" style="padding-top:10px"><div class="wrap"><div class="grid g3">{"".join(cards)}</div>
<div class="grid g2" style="margin-top:40px;align-items:start">
<div class="card"><h2 style="font-size:1.6rem">Enter a contest</h2>
<form class="form" data-lx="Contest entry" data-ok="Entry received! Good luck — winners are announced within 14 days of the closing date.">
<label class="f">Contest<select name="contest" required>{opts}</select></label>
<div class="row"><label class="f">Name<input name="name" required></label><label class="f">Email<input type="email" name="email" required></label></div>
<div class="row"><label class="f">Country<input name="country" required></label><label class="f">Age group<select name="age_group" required><option value="">Choose…</option><option>18–24</option><option>25–34</option><option>35–49</option><option>50+</option></select></label></div>
<label class="f">Link to your entry (video, doc, portfolio or streak screenshot)<input type="url" name="entry_link" required placeholder="https://"></label>
<label class="f">Tell us about your entry<textarea name="description" rows="3"></textarea></label>
<label class="chk" style="display:flex;gap:8px;font-size:.88rem"><input type="checkbox" required style="width:auto"> I am 18+ (or have a parent/guardian's permission), this is my own original work, and I accept the official rules.</label>
{honeypot()}<button class="btn signal block" type="submit">Submit my entry</button></form></div>
<div><div class="card"><h2 style="font-size:1.6rem">Sponsor a prize</h2><p>Put your brand in front of motivated learners. Prize sponsors get logo placement on the contest page, a mention in Express Weekly and winner announcements.</p><a class="btn ghost" href="partners.html">Sponsorship options</a> <a class="btn ghost" href="support.html">Fund the prize pool</a></div>
<div class="card" style="margin-top:16px"><h3>Official rules (summary)</h3><ul style="padding-left:1.1em;font-size:.92rem">
<li>No purchase or payment is necessary to enter or win. Contests are skill-based; winners are chosen by judges using the published criteria — not by chance.</li>
<li>Open to individuals 18+, or minors with verifiable parent/guardian consent, where permitted by law. Void where prohibited or restricted.</li>
<li>One entry per person per contest. Entries must be original and must not infringe anyone's rights.</li>
<li>Residents of jurisdictions with additional contest requirements (for example, Québec) may be subject to extra conditions; any required filings are made before prizes are awarded.</li>
<li>Prizes are non-transferable; cash alternatives at our discretion. Winners may be asked to answer a skill-testing question and sign a declaration.</li>
<li>Entrants grant Learning-Express a non-exclusive licence to display winning entries with credit.</li>
<li>Full terms: see our <a href="terms.html#contests">Terms of Use</a>.</li></ul></div></div></div>
</div></section>{nl_strip()}'''
    js = '''<script>(function(){var d=new Date(),m=d.toLocaleString("en",{month:"long"}),y=d.getFullYear(),last=new Date(y,d.getMonth()+1,0);var e=document.getElementById("cMonth");if(e)e.textContent=(m+" "+y+" CONTESTS").toUpperCase();var c=document.getElementById("cClose");if(c)c.textContent=last.toLocaleDateString("en",{month:"long",day:"numeric",year:"numeric"})+" (11:59 pm ET)";})();</script>'''
    emit("contests.html", page("contests.html", "Monthly Learning Contests & Prizes", "Free monthly skill contests for learners — Learning Streak Challenge, Explain-It-Simply video contest and more. Enter and win prizes.", body, extra_js=js), 0.7, ("Contests", "Monthly contests and prizes", "win prize challenge"))

def build_careers():
    roles = [
        ("Education writer (freelance)", "Remote · per article", "Research and write evidence-based guides and station notes in clear, friendly English. Teaching or subject expertise is a plus."),
        ("YouTube video creator / editor", "Remote · per project", "Script, record or edit short explainer videos and Shorts for our Express Lines."),
        ("Subject-matter reviewer", "Remote · hourly", "Experts in math, science, coding, finance, languages or health careers who check our routes for accuracy."),
        ("Partnerships & sponsorship associate", "Remote · commission", "Connect schools, edtech companies and brands with sponsorship and advertising opportunities."),
        ("Campus & community ambassador", "Remote · volunteer + perks", "Share Express Lines with your school or community, host study groups and run local challenges."),
        ("Volunteer translator", "Remote · volunteer", "Help translate guides into French, Spanish, Hindi and more."),
    ]
    rc = "".join(f'<div class="card"><span class="tag">{esc(m)}</span><h3 style="margin-top:8px">{esc(t)}</h3><p>{esc(d)}</p><a class="btn sm ghost" href="#apply" onclick="document.getElementById(\'roleSel\').value=\'{esc(t)}\'">Apply</a></div>' for t, m, d in roles)
    ro = "".join(f"<option>{esc(t)}</option>" for t, _, _ in roles)
    body = f'''<section class="hero" style="padding-bottom:24px"><div class="wrap" style="display:block"><div class="crumbs"><a href="index.html">Home</a> / Careers</div>
<span class="eyebrow">WE'RE HIRING TALENT</span><h1>Careers &amp; Creators</h1><p class="lead">Help millions learn faster. We work remotely with writers, educators, creators and community builders around the world.</p></div></section>
<section class="sec" style="padding-top:10px"><div class="wrap"><div class="grid g3">{rc}</div>
<div class="grid g2" style="margin-top:40px;align-items:start">
<div class="card" id="apply"><h2 style="font-size:1.6rem">Apply or join the talent pool</h2>
<form class="form" data-lx="Talent application" data-ok="Application received — thank you! If there's a fit we'll be in touch within 10 business days.">
<label class="f">Role<select name="role" id="roleSel"><option>General talent pool</option>{ro}</select></label>
<div class="row"><label class="f">Full name<input name="name" required></label><label class="f">Email<input type="email" name="email" required></label></div>
<div class="row"><label class="f">Location / time zone<input name="location"></label><label class="f">Availability<select name="availability"><option>A few hours a week</option><option>Part-time</option><option>Project-based</option><option>Full-time</option></select></label></div>
<label class="f">Portfolio, LinkedIn or YouTube link<input type="url" name="portfolio" placeholder="https://"></label>
<label class="f">Why you? (subjects, experience, ideas)<textarea name="pitch" rows="4" required></textarea></label>
{honeypot()}<button class="btn block" type="submit">Send application</button></form></div>
<div class="card"><h3>How we work</h3><ul style="padding-left:1.1em"><li>Remote-first, asynchronous</li><li>Clear briefs and fair, on-time pay for paid roles</li><li>Credit on everything you create</li><li>Accuracy and learner trust above everything</li></ul>
<h3>Hiring is funded by learners</h3><p class="note">A quarter of all support goes directly to paying creators. <a href="support.html">Support the crew</a>.</p></div></div>
</div></section>'''
    emit("careers.html", page("careers.html", "Careers: Writers, Video Creators, Tutors & Ambassadors", "Join Learning-Express as an education writer, YouTube creator, subject reviewer, partnerships associate, ambassador or volunteer translator.", body), 0.6, ("Careers", "Join as a writer, creator or tutor", "jobs hiring"))

def build_partners():
    pk = [("Line Sponsor", "Your brand on an entire Express Line page, its stations and related emails.", ["Logo + message on line page", "Mention in Express Weekly", "Monthly performance report"]),
          ("Contest Sponsor", "Fund the prizes for a monthly contest and reach motivated learners.", ["Logo on contest page", "Winner announcement credit", "Social shout-outs"]),
          ("Education Partner", "Receive opted-in, qualified learner inquiries from Program Match.", ["Matched by field, budget & region", "Explicit learner consent", "Pay-per-lead or flat fee"]),
          ("Newsletter & Display", "Sponsored placement in Express Weekly or direct banner placements.", ["Native newsletter slot", "Category targeting", "Clear sponsored labelling"])]
    cards = "".join(f'<div class="card"><h3>{esc(t)}</h3><p>{esc(d)}</p><ul style="padding-left:1.1em">{"".join(f"<li>{esc(x)}</li>" for x in li)}</ul></div>' for t, d, li in pk)
    body = f'''<section class="hero" style="padding-bottom:24px"><div class="wrap" style="display:block"><div class="crumbs"><a href="index.html">Home</a> / Partners</div>
<span class="eyebrow">PARTNERS · SPONSORS · ADVERTISERS</span><h1>Reach motivated learners</h1>
<p class="lead">Learning-Express visitors are actively building skills, choosing programs and changing careers. Partner with us through sponsorships, qualified program inquiries or advertising.</p>
<p><a class="btn signal" data-contact href="#" style="color:#fff">Contact about sponsorship / partnership</a> <a class="btn ghost" href="#pform">Send a brief</a></p></div></section>
<section class="sec" style="padding-top:10px"><div class="wrap"><div class="grid g4">{cards}</div>
<div class="card" id="pform" style="margin-top:36px;max-width:820px"><h2 style="font-size:1.6rem">Partnership brief</h2>
<form class="form" data-lx="Partner / advertiser inquiry" data-ok="Thanks! Our partnerships team will reply within 2 business days with availability and pricing.">
<div class="row"><label class="f">Organisation<input name="organisation" required></label><label class="f">Website<input type="url" name="website" placeholder="https://"></label></div>
<div class="row"><label class="f">Your name<input name="name" required></label><label class="f">Work email<input type="email" name="email" required></label></div>
<div class="row"><label class="f">Interested in<select name="interest"><option>Line sponsorship</option><option>Contest sponsorship</option><option>Education partner (Program Match leads)</option><option>Newsletter / display advertising</option><option>Acquiring this website / domain</option><option>Other partnership</option></select></label>
<label class="f">Monthly budget<select name="budget"><option>Under $500</option><option>$500 – $2,000</option><option>$2,000 – $10,000</option><option>$10,000+</option><option>Not sure</option></select></label></div>
<label class="f">Goals &amp; target audience<textarea name="details" rows="4"></textarea></label>{honeypot()}
<button class="btn block" type="submit">Send brief</button></form></div>
<p class="note" style="margin-top:20px">Sponsored content is always clearly labelled. Partners never influence our free recommendations.</p>
</div></section>'''
    emit("partners.html", page("partners.html", "Partners, Sponsorship & Advertising", "Sponsor an Express Line or contest, become an education partner for Program Match leads, or advertise to motivated learners.", body), 0.6, ("Partners & Advertising", "Sponsorship and partnership packages", "advertise sponsor"))

# ---------------------------------------------------------------- about, contact, legal
def simple(path, title, desc, inner, prio=0.4, crumbs=None, s=None):
    body = f'''<section class="sec"><div class="wrap narrow article"><div class="crumbs"><a href="index.html">Home</a> / {esc(crumbs or title)}</div>{inner}</div></section>'''
    emit(path, page(path, title, desc, body), prio, s)

def build_static():
    simple("about.html", "About Learning-Express", "Learning-Express is an independent, free learning hub that turns the best open-education resources into guided express lines.", f'''
<h1>About Learning-Express</h1>
<p class="lead">The web is full of excellent free lessons. What learners lack is a route. Learning-Express exists to give you one.</p>
<h2>What we do</h2>
<p>We design <a href="paths.html">Express Lines</a> — step-by-step routes to real outcomes — and fill each station with hand-picked resources from reputable open-education providers, universities and creators. We write original <a href="guides.html">study guides</a> grounded in learning science, build free <a href="tools.html">study tools</a>, publish a <a href="quiz.html">daily quiz</a> and curate fresh <a href="videos.html">video lessons</a> and <a href="news.html">education news</a> every day.</p>
<h2>Our principles</h2>
<ul><li><strong>Free first.</strong> Every line can be completed without paying.</li><li><strong>Credit creators.</strong> We link to original sources and embed videos only through official players.</li><li><strong>Evidence over hype.</strong> Techniques we recommend are supported by learning research.</li><li><strong>Honest monetisation.</strong> We are funded by advertising, optional support and clearly-disclosed partners. Partners never decide our free recommendations.</li></ul>
<h2>How we choose resources</h2>
<p>Resources must be free to access (or free to audit), come from a credible provider, be current and match the station's outcome. We review lines regularly and welcome corrections through our <a href="contact.html">contact form</a>.</p>
<h2>Independence</h2>
<p>Learning-Express is an independent website. It is not affiliated with EBSCO, “LearningExpress”, “LearningExpress Library” or any organisation whose resources we link to. See our <a href="disclaimer.html">disclaimer and trademark notice</a>.</p>
<p><a class="btn" href="contact.html">Get in touch</a></p>''', 0.5, s=("About", "About Learning-Express"))

    simple("contact.html", "Contact Learning-Express", "Contact Learning-Express for questions, corrections, partnerships, sponsorship, advertising or press.", f'''
<h1>Contact us</h1><p class="lead">Questions, corrections, partnership ideas or press — we read everything and reply within 1–2 business days.</p>
<div class="card"><form class="form" data-lx="Contact form" data-keep>
<div class="row"><label class="f">Name<input name="name" required autocomplete="name"></label><label class="f">Email<input type="email" name="email" required autocomplete="email"></label></div>
<label class="f">Topic<select name="topic" id="ctTopic"><option value="question">General question</option><option value="correction">Correction or broken link</option><option value="partnership">Partnership / sponsorship / advertising</option><option value="domain">Interested in this website / domain</option><option value="press">Press / news tip</option><option value="creator">Creator or tutor</option><option value="other">Other</option></select></label>
<label class="f">Message<textarea name="message" rows="6" required></textarea></label>{honeypot()}
<button class="btn block" type="submit">Send message</button>
<p class="note">We use your details only to reply. See our <a href="privacy.html">Privacy Policy</a>.</p></form></div>
<div class="card" style="margin-top:20px"><h3>Business inquiries</h3><p>Interested in this website, the domain name, sponsorship, advertising or a partnership?</p><a class="btn ghost" data-contact href="#">Contact the owner directly</a></div>
<script>(function(){{var t=new URLSearchParams(location.search).get("topic");if(t){{var s=document.getElementById("ctTopic");if(s)s.value=t;}}}})();</script>''', 0.5, s=("Contact", "Contact the team"))

    simple("privacy.html", "Privacy Policy", "How Learning-Express collects, uses and protects information, including cookies and Google AdSense advertising.", f'''
<h1>Privacy Policy</h1><p class="note">Last updated: {datetime.date.today().strftime("%B %d, %Y")}</p>
<p>This policy explains what information Learning-Express (“we”, “us”) collects when you use this website, how we use it and the choices you have.</p>
<h2>Information you give us</h2>
<p>When you submit a form — newsletter, Program Match, contact, contest entry, donation pledge or job application — we collect the details you enter, such as your name, email address and answers. Form submissions are delivered to us by a third-party form-processing service (FormSubmit). We use this information only to respond, deliver what you asked for, run contests and, for Program Match, to prepare your shortlist.</p>
<p><strong>Program Match partner sharing:</strong> we share your answers with education partners <em>only</em> if you tick the optional consent box, and only with up to three relevant partners. You can withdraw consent at any time by contacting us.</p>
<h2>Information stored on your device</h2>
<p>Progress check-offs, flashcard decks, quiz scores, streaks, theme and cookie choices are stored in your browser's local storage. This data stays on your device; we do not receive it.</p>
<h2 id="cookies">Cookies and advertising</h2>
<p>We use Google AdSense to show advertisements. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visit to this site and/or other sites on the Internet.</p>
<p>You may opt out of personalised advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a>, or opt out of some third-party vendors' use of cookies for personalised advertising at <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">www.aboutads.info</a>. Learn more in <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">How Google uses information from sites that use its services</a>.</p>
<p>Selecting “Essential only” in our cookie banner requests non-personalised ads. Visitors in the EEA, UK and Switzerland may be shown a consent message managed through Google's certified consent tools.</p>
<h2>Embedded content</h2>
<p>Videos are embedded using YouTube's privacy-enhanced mode (youtube-nocookie.com) and load only when you press play. Once played, YouTube's own privacy policy applies. Fonts are served by Google Fonts.</p>
<h2>Children</h2>
<p>This site is intended for a general audience and is not directed at children under 13. We do not knowingly collect personal information from children under 13. Parents who believe a child has submitted information can contact us for deletion.</p>
<h2>Your rights</h2>
<p>Depending on where you live (for example under GDPR, UK GDPR, PIPEDA, Québec Law 25 or US state laws), you may have rights to access, correct, delete or restrict use of your personal information and to withdraw consent. Contact us through the <a href="contact.html">contact form</a> to make a request.</p>
<h2>Retention and security</h2>
<p>We keep form submissions only as long as needed for the purpose collected, and use reasonable safeguards. No method of transmission over the Internet is 100% secure.</p>
<h2>Changes</h2><p>We may update this policy; the date above shows the latest version.</p>
<h2>Contact</h2><p>Questions about privacy? Use our <a href="contact.html">contact form</a>.</p>''', 0.3, s=("Privacy Policy", "Privacy, cookies and AdSense"))

    simple("terms.html", "Terms of Use", "Terms governing use of the Learning-Express website, tools, contests and Program Match.", f'''
<h1>Terms of Use</h1><p class="note">Last updated: {datetime.date.today().strftime("%B %d, %Y")}</p>
<h2>1. Acceptance</h2><p>By using Learning-Express you agree to these terms. If you do not agree, please do not use the site.</p>
<h2>2. Educational information only</h2><p>Content is provided for general educational purposes. It is not professional, medical, legal, financial or career advice. Outcomes depend on many factors outside our control.</p>
<h2>3. Third-party resources</h2><p>We link to and embed resources from third parties. We do not control and are not responsible for their content, availability, pricing or policies. Links do not imply endorsement by or affiliation with those parties.</p>
<h2>4. Program Match</h2><p>Program Match suggestions are informational. We do not guarantee admission, outcomes or the quality of any third-party program. Verify accreditation, costs and terms directly with providers before enrolling. We may receive compensation from partners when you opt in to be contacted; this is disclosed on the Program Match page.</p>
<h2 id="contests">5. Contests</h2><p>Contests are skill-based and free to enter; no purchase or payment is necessary. Eligibility, entry periods, judging criteria and prizes are described on the <a href="contests.html">Contests page</a> and form part of these terms. We may cancel, modify or suspend a contest if it cannot run as planned, and may disqualify entries that are fraudulent, plagiarised or violate these terms. Winners are responsible for any applicable taxes. Void where prohibited.</p>
<h2>6. Donations and pledges</h2><p>Support is voluntary and non-refundable once processed, except where required by law. Learning-Express is not a registered charity and contributions are not tax-deductible.</p>
<h2>7. Acceptable use</h2><p>Do not misuse the site, submit spam or unlawful content, attempt to disrupt service, or scrape content at scale.</p>
<h2>8. Intellectual property</h2><p>Original text, guides, routes, tools and design on this site are owned by Learning-Express. Third-party names, logos and content belong to their owners. See our <a href="disclaimer.html">disclaimer and trademark notice</a>.</p>
<h2>9. Disclaimer and limitation of liability</h2><p>The site is provided “as is” without warranties. To the fullest extent permitted by law, we are not liable for indirect or consequential losses arising from use of the site.</p>
<h2>10. Changes</h2><p>We may update these terms. Continued use after changes means you accept them.</p>''', 0.3, s=("Terms of Use", "Site terms and contest rules"))

    simple("disclaimer.html", "Disclaimer, Trademark & Copyright Notice", "Independence, trademark and copyright disclosure for Learning-Express.", '''
<h1>Disclaimer, Trademark &amp; Copyright Notice</h1>
<h2>Independence and no affiliation</h2>
<p>Learning-Express (the hyphenated name of this website and its domain) is an independent, free educational resource. <strong>It is not affiliated with, endorsed by, sponsored by or connected to EBSCO Information Services, EBSCO Industries, “LearningExpress”, “LearningExpress, LLC”, “LearningExpress Library”, or any of their products or services.</strong> Those names are trademarks of their respective owners. We do not offer their products, do not use their content and do not represent ourselves as them. If you are looking for that service, please contact your library or the company directly.</p>
<p>Likewise, we are not affiliated with any university, course platform, test publisher, government agency or YouTube creator mentioned on this site.</p>
<h2>Third-party trademarks</h2>
<p>All product names, logos and brands referenced (for example Khan Academy, Coursera, edX, freeCodeCamp, OpenStax, MIT OpenCourseWare, Google, Microsoft, YouTube, Duolingo and others) are property of their respective owners and are used only to identify the free resources we link to — nominative use that implies no endorsement. Exam and test names such as SAT®, GED® and others are registered trademarks of their owners, none of whom are involved with or endorse this site.</p>
<h2>Copyright</h2>
<p>Original guides, routes, station descriptions, quiz questions, tools, code and design on Learning-Express are © Learning-Express. You may link to any page and quote brief excerpts with attribution. Embedded videos are streamed from YouTube using its official embed player and remain the property of their creators; we do not host or download them. News headlines link to the original publishers and display only titles and brief excerpts.</p>
<h2>Copyright or trademark concerns</h2>
<p>If you believe content on this site infringes your rights, please use our <a href="contact.html?topic=correction">contact form</a> with details of the work, the page URL and your contact information. We review notices promptly and remove or correct material where appropriate.</p>
<h2>Educational disclaimer</h2>
<p>Information is for general education only and is not professional advice. Health-careers content is career education, not medical guidance. Finance content is not investment advice.</p>
<h2>Advertising disclosure</h2>
<p>This site displays advertising through Google AdSense and may receive compensation from education partners when learners opt in through Program Match. Sponsored placements are always labelled.</p>''', 0.3, s=("Disclaimer & Trademarks", "Independence and trademark notice"))

    emit("404.html", page("404.html", "Page not found", "This station doesn't exist.", '''<section class="sec"><div class="wrap narrow center"><span class="eyebrow">404 · WRONG PLATFORM</span><h1>This station doesn't exist.</h1><p class="lead">The page may have moved. Let's get you back on a line.</p><p><a class="btn" href="index.html">Home</a> <a class="btn ghost" href="paths.html">Express Lines</a></p></div></section>'''), 0.0)

# ---------------------------------------------------------------- write
def write_all():
    for path, (h, _) in OUT.items():
        with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
            f.write(h)
    urls = "".join(f"<url><loc>{SITE_URL}/{'' if p=='index.html' else p}</loc><lastmod>{TODAY}</lastmod><priority>{pr:.1f}</priority></url>" for p, (_, pr) in sorted(OUT.items(), key=lambda x: -x[1][1]) if p != "404.html")
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    with open(os.path.join(ROOT, "data", "search.json"), "w") as f:
        json.dump(SEARCH, f, ensure_ascii=False)
    print(f"Built {len(OUT)} pages.")

if __name__ == "__main__":
    build_home(); build_lines(); build_guides(); build_videos(); build_news(); build_tools(); build_quiz(); build_planner()
    build_match(); build_support(); build_contests(); build_careers(); build_partners(); build_static()
    write_all()
