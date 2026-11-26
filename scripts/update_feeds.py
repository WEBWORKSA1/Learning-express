#!/usr/bin/env python3
"""Daily auto-refresh: pulls latest YouTube lessons + education news (RSS/Atom) into data/*.json.
Stdlib only, fault-tolerant: a failing source is logged and skipped; previous data is kept if everything fails."""
import json, os, re, sys, html, datetime, urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")
UA = "Mozilla/5.0 (compatible; LearningExpressBot/1.0; +https://github.com/WEBWORKSA1/learning-express)"
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
      "media": "http://search.yahoo.com/mrss/", "dc": "http://purl.org/dc/elements/1.1/",
      "content": "http://purl.org/rss/1.0/modules/content/"}

def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def clean(s, n=240):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(re.sub(r"\s+", " ", s)).strip()
    return (s[: n - 1] + "…") if len(s) > n else s

def iso(s):
    if not s:
        return ""
    s = s.strip()
    try:
        return parsedate_to_datetime(s).astimezone(datetime.timezone.utc).isoformat()
    except Exception:
        pass
    try:
        return datetime.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(datetime.timezone.utc).isoformat()
    except Exception:
        return ""

def load(name, default):
    try:
        with open(os.path.join(DATA, name), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save(name, obj):
    with open(os.path.join(DATA, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)

def videos(src):
    items, chans, log = [], [], []
    for ch in src["channels"]:
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={ch['id']}"
        try:
            root = ET.fromstring(fetch(url))
            n = 0
            for e in root.findall("a:entry", NS):
                vid = e.findtext("yt:videoId", default="", namespaces=NS)
                title = e.findtext("a:title", default="", namespaces=NS)
                link = e.find("a:link", NS)
                href = link.get("href") if link is not None else ""
                if not vid or "/shorts/" in href or "#shorts" in title.lower():
                    continue
                desc = e.findtext("media:group/media:description", default="", namespaces=NS)
                items.append({"id": vid, "title": clean(title, 140), "channel": ch["name"], "cats": ch["cats"],
                              "date": iso(e.findtext("a:published", default="", namespaces=NS)), "desc": clean(desc, 160)})
                n += 1
                if n >= 6:
                    break
            chans.append({"name": ch["name"], "id": ch["id"], "cats": ch["cats"], "ok": n > 0})
            log.append(f"OK   {ch['name']}: {n}")
        except Exception as ex:
            chans.append({"name": ch["name"], "id": ch["id"], "cats": ch["cats"], "ok": False})
            log.append(f"FAIL {ch['name']}: {ex}")
    items.sort(key=lambda v: v["date"], reverse=True)
    return items[:180], chans, log

def news(src):
    items, log = [], []
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=45)
    for fd in src["feeds"]:
        try:
            root = ET.fromstring(fetch(fd["url"]))
            got = 0
            entries = root.findall(".//item") or root.findall("a:entry", NS)
            for e in entries[:12]:
                if e.tag == "item":
                    title = e.findtext("title", "")
                    link = e.findtext("link", "")
                    date = iso(e.findtext("pubDate", "") or e.findtext("dc:date", "", NS))
                    summ = e.findtext("description", "")
                else:
                    title = e.findtext("a:title", "", NS)
                    l = e.find("a:link[@rel='alternate']", NS)
                    if l is None:
                        l = e.find("a:link", NS)
                    link = l.get("href") if l is not None else ""
                    date = iso(e.findtext("a:published", "", NS) or e.findtext("a:updated", "", NS))
                    summ = e.findtext("a:summary", "", NS) or e.findtext("a:content", "", NS)
                if not title or not link.startswith("http"):
                    continue
                if date:
                    try:
                        if datetime.datetime.fromisoformat(date) < cutoff:
                            continue
                    except Exception:
                        pass
                items.append({"title": clean(title, 160), "link": link.strip(), "date": date, "source": fd["name"], "summary": clean(summ, 220)})
                got += 1
            log.append(f"OK   {fd['name']}: {got}")
        except Exception as ex:
            log.append(f"FAIL {fd['name']}: {ex}")
    seen, out = set(), []
    for it in sorted(items, key=lambda x: x["date"], reverse=True):
        k = it["title"].lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(it)
    return out[:80], log

def main():
    src = load("sources.json", {"channels": [], "feeds": []})
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    v, chans, vlog = videos(src)
    n, nlog = news(src)
    print("\n".join(vlog + nlog))
    if v:
        save("videos.json", {"updated": now, "items": v, "channels": chans})
    else:
        print("No videos fetched; keeping previous file.")
    if n:
        save("news.json", {"updated": now, "items": n})
    else:
        print("No news fetched; keeping previous file.")

if __name__ == "__main__":
    main()
