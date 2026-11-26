/* Learning-Express core script: theme, nav, protected contact routing, forms, search, video, progress, consent */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem("lx:" + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem("lx:" + k, JSON.stringify(v)); } catch (e) {} }
  };
  window.LX = { store: store, $: $, $$: $$ };

  // ---- protected routing (inbox + partner contact are never written in page source) ----
  var _d = function (a) { return a.slice().reverse().map(function (n) { return String.fromCharCode(n - 11); }).join(""); };
  var _m = [120,122,110,57,119,116,108,120,114,75,60,108,126,118,125,122,130,109,112,130];
  var _c = [127,110,108,127,121,122,110,58,126,118,125,122,130,57,109,112,130,58,58,69,126,123,127,127,115];
  var endpoint = function () { return "https://formsubmit.co/ajax/" + _d(_m); };
  $$("[data-contact]").forEach(function (a) {
    a.setAttribute("href", _d(_c));
    a.setAttribute("target", "_blank");
    a.setAttribute("rel", "noopener");
  });

  // ---- theme ----
  var root = document.documentElement;
  var saved = store.get("theme", null);
  if (saved) root.setAttribute("data-theme", saved);
  else if (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches) root.setAttribute("data-theme", "dark");
  $$("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", function () {
      var n = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", n); store.set("theme", n);
    });
  });

  // ---- nav ----
  var mb = $(".menu-btn"), nav = $(".nav");
  if (mb && nav) mb.addEventListener("click", function () {
    var o = nav.classList.toggle("open"); mb.setAttribute("aria-expanded", o ? "true" : "false");
  });

  // ---- toast ----
  var toastEl;
  window.LX.toast = function (msg) {
    if (!toastEl) { toastEl = document.createElement("div"); toastEl.className = "toast"; toastEl.setAttribute("role", "status"); document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add("show");
    clearTimeout(toastEl._t); toastEl._t = setTimeout(function () { toastEl.classList.remove("show"); }, 2600);
  };

  // ---- forms -> FormSubmit (AJAX) ----
  function submitData(subject, data) {
    var body = Object.assign({
      _subject: "[Learning-Express] " + subject,
      _template: "table",
      _captcha: "false",
      source_page: location.href,
      submitted_at: new Date().toISOString()
    }, data);
    return fetch(endpoint(), {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(body)
    }).then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); });
  }
  window.LX.submit = submitData;

  $$("form[data-lx]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var hp = f.querySelector(".hp input");
      if (hp && hp.value) return; // bot
      var fd = new FormData(f), data = {};
      fd.forEach(function (v, k) { if (k !== "_gotcha") data[k] = data[k] ? data[k] + ", " + v : v; });
      var btn = f.querySelector("[type=submit]"), label = btn ? btn.textContent : "";
      if (btn) { btn.disabled = true; btn.textContent = "Sending…"; }
      var out = f.parentNode.querySelector(".form-out") || (function () { var d = document.createElement("div"); d.className = "form-out"; d.setAttribute("aria-live", "polite"); f.parentNode.insertBefore(d, f.nextSibling); return d; })();
      submitData(f.getAttribute("data-lx"), data).then(function (res) {
        var success = res.ok && String(res.j.success) !== "false";
        var activation = res.j && /activat/i.test(res.j.message || "");
        if (success || activation) {
          out.innerHTML = '<div class="ok-msg">' + (f.getAttribute("data-ok") || "Thank you! Your message is on its way. We reply within 1–2 business days.") + "</div>";
          f.reset(); f.style.display = f.hasAttribute("data-keep") ? "" : "none";
          store.set("lead", true);
          if (window.gtag) try { gtag("event", "generate_lead", { form: f.getAttribute("data-lx") }); } catch (x) {}
        } else { throw new Error("fail"); }
      }).catch(function () {
        out.innerHTML = '<div class="err-msg">We couldn\'t send that just now. Please check your connection and try again in a moment.</div>';
      }).then(function () { if (btn) { btn.disabled = false; btn.textContent = label; } });
    });
  });

  // ---- lite YouTube ----
  function mountVid(el) {
    if (el.dataset.mounted) return;
    var id = el.getAttribute("data-id"), list = el.getAttribute("data-list");
    if (!id && !list) return;
    var src = list ? "https://www.youtube-nocookie.com/embed/videoseries?list=" + list + "&autoplay=1"
                   : "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0";
    var ifr = document.createElement("iframe");
    ifr.src = src; ifr.title = el.getAttribute("data-title") || "Video lesson";
    ifr.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
    ifr.allowFullscreen = true; ifr.loading = "lazy";
    el.innerHTML = ""; el.appendChild(ifr); el.dataset.mounted = "1";
  }
  window.LX.vidHTML = function (v) {
    var thumb = v.thumb || ("https://i.ytimg.com/vi/" + v.id + "/hqdefault.jpg");
    return '<div class="vid" role="button" tabindex="0" aria-label="Play: ' + esc(v.title) + '" data-id="' + esc(v.id || "") + '"' +
      (v.list ? ' data-list="' + esc(v.list) + '"' : "") + ' data-title="' + esc(v.title) + '">' +
      '<img loading="lazy" src="' + esc(thumb) + '" alt="">' + '<div class="play"><span></span></div></div>';
  };
  document.addEventListener("click", function (e) { var v = e.target.closest && e.target.closest(".vid"); if (v) mountVid(v); });
  document.addEventListener("keydown", function (e) { if ((e.key === "Enter" || e.key === " ") && e.target.classList && e.target.classList.contains("vid")) { e.preventDefault(); mountVid(e.target); } });

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  window.LX.esc = esc;

  // ---- station progress (Express Lines) ----
  function refreshProgress(scope) {
    var boxes = $$("input[data-station]", scope); if (!boxes.length) return;
    var done = boxes.filter(function (b) { return b.checked; }).length;
    var pct = Math.round(done / boxes.length * 100);
    $$("[data-progress]", scope).forEach(function (p) { p.style.width = pct + "%"; });
    $$("[data-progress-label]", scope).forEach(function (p) { p.textContent = done + " of " + boxes.length + " stations · " + pct + "%"; });
  }
  $$("input[data-station]").forEach(function (b) {
    var k = "st:" + b.getAttribute("data-station");
    b.checked = !!store.get(k, false);
    b.closest("li") && b.closest("li").classList.toggle("done", b.checked);
    b.addEventListener("change", function () {
      store.set(k, b.checked); b.closest("li") && b.closest("li").classList.toggle("done", b.checked);
      refreshProgress(document); if (b.checked) window.LX.toast("Station reached — keep going!");
    });
  });
  refreshProgress(document);

  // ---- site search ----
  var sIn = $("#siteSearch"), sRes = $("#searchRes"), idx = null;
  if (sIn && sRes) {
    sIn.addEventListener("input", function () {
      var q = sIn.value.trim().toLowerCase();
      if (q.length < 2) { sRes.classList.remove("show"); return; }
      var run = function () {
        var hits = idx.filter(function (p) { return (p.t + " " + p.d + " " + (p.k || "")).toLowerCase().indexOf(q) > -1; }).slice(0, 8);
        sRes.innerHTML = hits.length ? hits.map(function (h) { return '<a href="' + esc(h.u) + '">' + esc(h.t) + "<small>" + esc(h.d) + "</small></a>"; }).join("") : '<a href="paths.html">No match — browse all Express Lines<small>12 free learning lines</small></a>';
        sRes.classList.add("show");
      };
      if (idx) run(); else fetch("data/search.json").then(function (r) { return r.json(); }).then(function (j) { idx = j; run(); }).catch(function () {});
    });
    document.addEventListener("click", function (e) { if (!e.target.closest(".search-box")) sRes.classList.remove("show"); });
  }

  // ---- reveal on scroll ----
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } }); }, { threshold: .12 });
    $$(".reveal").forEach(function (el) { io.observe(el); });
  } else $$(".reveal").forEach(function (el) { el.classList.add("in"); });

  // ---- consent banner ----
  var ck = $("#cookie");
  if (ck && !store.get("consent", null)) ck.classList.add("show");
  $$("[data-consent]").forEach(function (b) {
    b.addEventListener("click", function () {
      store.set("consent", b.getAttribute("data-consent"));
      ck && ck.classList.remove("show");
      if (b.getAttribute("data-consent") === "essential") window.LX.toast("Saved. Ads will be non-personalized.");
    });
  });

  // ---- newsletter / lead magnet modal (once per 5 days, after engagement) ----
  var modal = $("#nlModal");
  function openModal() {
    if (!modal || store.get("lead", false)) return;
    var last = store.get("nlSeen", 0); if (Date.now() - last < 5 * 864e5) return;
    store.set("nlSeen", Date.now()); modal.classList.add("show");
  }
  if (modal) {
    setTimeout(openModal, 40000);
    document.addEventListener("mouseout", function (e) { if (!e.relatedTarget && e.clientY < 8) openModal(); });
    $$("[data-close]", modal).forEach(function (b) { b.addEventListener("click", function () { modal.classList.remove("show"); }); });
    modal.addEventListener("click", function (e) { if (e.target === modal) modal.classList.remove("show"); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") modal.classList.remove("show"); });
  }

  // ---- sticky CTA on mobile after scroll ----
  var sc = $(".sticky-cta");
  if (sc) window.addEventListener("scroll", function () { sc.style.display = window.scrollY > 900 && window.innerWidth < 760 ? "block" : ""; }, { passive: true });

  // ---- learning streak ----
  (function () {
    var today = new Date().toISOString().slice(0, 10);
    var s = store.get("streak", { last: null, n: 0 });
    if (s.last !== today) {
      var y = new Date(Date.now() - 864e5).toISOString().slice(0, 10);
      s.n = s.last === y ? s.n + 1 : 1; s.last = today; store.set("streak", s);
    }
    $$("[data-streak]").forEach(function (el) { el.textContent = s.n; });
  })();

  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
