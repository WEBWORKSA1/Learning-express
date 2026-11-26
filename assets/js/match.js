/* Program Match lead funnel */
(function () {
  var LX = window.LX, esc = LX.esc;
  var steps = Array.prototype.slice.call(document.querySelectorAll(".step")), total = steps.length, cur = 1, ans = {};
  var bar = document.getElementById("fBar"), lbl = document.getElementById("fStepLbl"), back = document.getElementById("fBack");
  var LINE = { web: ["path-web.html", "Coding & Web Dev Line"], ai: ["path-ai.html", "AI & Prompting Line"], care: ["path-health-careers.html", "Health & Care Careers Line"], biz: ["path-business.html", "Business & Entrepreneurship Line"], mkt: ["path-marketing.html", "Digital Marketing Line"], fin: ["path-finance.html", "Personal Finance & Investing Line"], edu: ["path-study-skills.html", "Study Skills Line"], trades: ["path-math.html", "Math Foundations Line"], lang: ["path-languages.html", "Language Learning Line"], unsure: ["path-career.html", "Career Launch & Interview Line"], data: ["path-data.html", "Data, Excel & SQL Line"], job: ["path-career.html", "Career Launch & Interview Line"], study: ["path-study-skills.html", "Study Skills Line"], math: ["path-math.html", "Math Foundations Line"], sci: ["path-science.html", "Science Essentials Line"] };
  var LABEL = {};
  document.querySelectorAll(".opt").forEach(function (o) { LABEL[o.closest(".step").getAttribute("data-key") + ":" + o.getAttribute("data-v")] = o.textContent.trim(); });

  function go(n) {
    cur = Math.max(1, Math.min(total, n));
    steps.forEach(function (s) { s.classList.toggle("on", +s.getAttribute("data-step") === cur); });
    bar.style.width = Math.round(cur / total * 100) + "%"; lbl.textContent = "Step " + cur + " of " + total;
    back.style.visibility = cur > 1 ? "visible" : "hidden";
    if (cur === total) preview();
    var f = document.getElementById("funnel"); if (f && f.getBoundingClientRect().top < 0) f.scrollIntoView({ behavior: "smooth" });
  }
  function types() {
    var t = [], b = ans.budget, g = ans.goal;
    if (b === "free") t.push("Free courses & audit-track university courses");
    if (g === "degree") t.push("Accredited online degree or diploma programs");
    if (g === "exam") t.push("Exam-prep courses & official practice materials");
    if (g === "career" || g === "promotion") t.push(b === "15k+" || b === "5-15k" ? "Career bootcamps with job support" : "Professional certificates (industry-issued)");
    if (g === "business") t.push("Short practical business & marketing courses");
    if (g === "child") t.push("Tutoring & K-12 learning platforms");
    if (b === "aid") t.push("Programs with financial aid, grants or employer funding");
    if (!t.length) t.push("Professional certificates", "Short online courses");
    return t;
  }
  function score() { var s = 0; if (ans.timeline === "now") s += 3; else if (ans.timeline === "1-3m") s += 2; else if (ans.timeline === "3-6m") s += 1;
    if (["1-5k", "5-15k", "15k+"].indexOf(ans.budget) > -1) s += 2; if (ans.budget === "aid") s += 1; if (["degree", "career", "exam"].indexOf(ans.goal) > -1) s += 1;
    return s >= 5 ? "HOT" : s >= 3 ? "WARM" : "NURTURE"; }
  function preview() { var L = LINE[ans.field] || LINE.unsure; document.getElementById("fPreview").innerHTML = "✓ Your match is ready: <strong>" + esc(types()[0]) + "</strong> + a free starter route on the <strong>" + esc(L[1]) + "</strong>."; }

  steps.forEach(function (s) {
    var key = s.getAttribute("data-key"); if (!key) return;
    s.querySelectorAll(".opt").forEach(function (o) {
      o.addEventListener("click", function () {
        s.querySelectorAll(".opt").forEach(function (x) { x.setAttribute("aria-pressed", x === o ? "true" : "false"); });
        ans[key] = o.getAttribute("data-v"); setTimeout(function () { go(+s.getAttribute("data-step") + 1); }, 180);
      });
    });
  });
  back.addEventListener("click", function () { go(cur - 1); });

  // deep-link prefill (?goal= / ?field=)
  var qp = new URLSearchParams(location.search), start = 1;
  ["goal", "field"].forEach(function (k, idx) { var v = qp.get(k); if (!v) return; var o = document.querySelector('.step[data-key="' + k + '"] .opt[data-v="' + v + '"]'); if (o) { o.setAttribute("aria-pressed", "true"); ans[k] = v; if (start === idx + 1) start = idx + 2; } });
  go(start);

  document.getElementById("fForm").addEventListener("submit", function (e) {
    e.preventDefault(); var f = this; if (f.querySelector(".hp input").value) return;
    var fd = new FormData(f), data = {}; fd.forEach(function (v, k) { if (k !== "_gotcha") data[k] = v; });
    ["goal", "field", "level", "format", "budget", "timeline"].forEach(function (k) { data["answer_" + k] = LABEL[k + ":" + ans[k]] || ans[k] || "-"; });
    data.lead_score = score(); data.recommended = types().join(" | "); data.partner_consent = data.partner_consent || "no";
    var btn = f.querySelector("[type=submit]"); btn.disabled = true; btn.textContent = "Preparing your shortlist…";
    LX.submit("Program Match lead — " + data.lead_score + " — " + (data.answer_field || ""), data).then(function (r) {
      var ok = r.ok && String(r.j.success) !== "false" || /activat/i.test((r.j && r.j.message) || "");
      if (!ok) throw 0; LX.store.set("lead", true); render(data);
    }).catch(function () { btn.disabled = false; btn.textContent = "Get my free shortlist →"; LX.toast("Connection issue — please try again."); });
  });

  function render(data) {
    var L = LINE[ans.field] || LINE.unsure;
    document.getElementById("fForm").style.display = "none"; document.getElementById("fPreview").style.display = "none";
    document.querySelector(".step.on h3").textContent = "Your Program Match, " + (data.first_name || "") + " 🎉";
    document.getElementById("fResult").innerHTML =
      '<div class="ok-msg" style="margin-bottom:16px">Your full shortlist is on its way to your inbox.</div>' +
      "<h4>Recommended program types</h4><ul>" + types().map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") + "</ul>" +
      '<h4>Start free today</h4><p><a class="btn" href="' + L[0] + '">Ride the ' + esc(L[1]) + " →</a></p>" +
      '<h4>Before you enrol anywhere</h4><p class="note">Use our checklist: <a href="guide-choose-online-program.html">How to choose an online program</a> — accreditation, outcomes, total cost and red flags.</p>' +
      (data.partner_consent === "yes" ? '<p class="note">Up to 3 relevant education partners may contact you. You can opt out anytime.</p>' : '<p class="note">You chose not to be contacted by partners — only we will email you.</p>');
    bar.style.width = "100%"; lbl.textContent = "Complete"; back.style.visibility = "hidden";
  }
})();
