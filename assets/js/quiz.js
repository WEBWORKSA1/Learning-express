/* Daily Express Quiz — deterministic daily set + topic practice */
(function () {
  var LX = window.LX, esc = LX.esc, store = LX.store, box = document.getElementById("quizBox");
  var today = new Date().toISOString().slice(0, 10);
  function seeded(seed) { var s = 0; for (var i = 0; i < seed.length; i++) s = (s * 31 + seed.charCodeAt(i)) >>> 0; return function () { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
  function pick(bank, n, seed) { var r = seeded(seed), arr = bank.slice(); for (var i = arr.length - 1; i > 0; i--) { var j = Math.floor(r() * (i + 1)); var t = arr[i]; arr[i] = arr[j]; arr[j] = t; } return arr.slice(0, n); }
  var stats = store.get("quiz", { best: null, done: 0, last: null });
  function paintStats() { document.getElementById("qBest").textContent = stats.best == null ? "–" : stats.best + "/5"; document.getElementById("qDone").textContent = stats.done; }
  paintStats();

  fetch("data/quiz.json").then(function (r) { return r.json(); }).then(function (bank) {
    var cats = []; bank.forEach(function (q) { if (cats.indexOf(q.c) < 0) cats.push(q.c); });
    document.getElementById("qTopics").innerHTML = '<button class="chip" data-c="__daily" aria-pressed="true">Today\'s quiz</button>' + cats.map(function (c) { return '<button class="chip" data-c="' + esc(c) + '" aria-pressed="false">' + esc(c) + "</button>"; }).join("");
    document.getElementById("qTopics").addEventListener("click", function (e) {
      var b = e.target.closest(".chip"); if (!b) return;
      document.querySelectorAll("#qTopics .chip").forEach(function (c) { c.setAttribute("aria-pressed", c === b ? "true" : "false"); });
      var c = b.getAttribute("data-c");
      if (c === "__daily") run(pick(bank, 5, today), true, "Today's quiz · " + new Date().toLocaleDateString("en", { weekday: "long", month: "long", day: "numeric" }));
      else run(pick(bank.filter(function (q) { return q.c === c; }), 5, c + Date.now()), false, c + " practice");
    });
    run(pick(bank, 5, today), true, "Today's quiz · " + new Date().toLocaleDateString("en", { weekday: "long", month: "long", day: "numeric" }));
  }).catch(function () { box.innerHTML = '<p class="err-msg">The quiz could not load. Please refresh.</p>'; });

  function run(qs, daily, title) {
    var i = 0, score = 0;
    function q() {
      var Q = qs[i];
      box.innerHTML = '<span class="tag" style="font:700 .75rem var(--f-mono);color:var(--signal)">' + esc(title).toUpperCase() + "</span>" +
        '<div class="progress" style="margin:12px 0 18px"><i style="width:' + (i / qs.length * 100) + '%"></i></div>' +
        '<p class="note mb0">Question ' + (i + 1) + " of " + qs.length + " · " + esc(Q.c) + '</p><h2 style="font-size:1.45rem;margin-top:6px">' + esc(Q.q) + '</h2><div class="q-opts">' +
        Q.o.map(function (o, k) { return '<button class="q-opt" data-k="' + k + '">' + String.fromCharCode(65 + k) + ". " + esc(o) + "</button>"; }).join("") + '</div><div id="qFb"></div>';
      box.querySelectorAll(".q-opt").forEach(function (b) {
        b.onclick = function () {
          var k = +b.getAttribute("data-k"), right = k === Q.a; if (right) score++;
          box.querySelectorAll(".q-opt").forEach(function (x) { x.disabled = true; var kk = +x.getAttribute("data-k"); if (kk === Q.a) x.classList.add("right"); else if (kk === k) x.classList.add("wrong"); });
          document.getElementById("qFb").innerHTML = '<div class="' + (right ? "ok-msg" : "err-msg") + '" style="margin-bottom:12px">' + (right ? "✓ Correct! " : "✗ Not quite. ") + '<span style="font-weight:400">' + esc(Q.e) + "</span></div>" +
            '<button class="btn" id="qNext">' + (i < qs.length - 1 ? "Next question →" : "See my score") + "</button>";
          document.getElementById("qNext").onclick = function () { i++; i < qs.length ? q() : end(); };
        };
      });
    }
    function end() {
      if (daily) { stats.done++; stats.last = today; if (stats.best == null || score > stats.best) stats.best = score; store.set("quiz", stats); paintStats(); }
      var msg = score === 5 ? "Perfect score! 🏆" : score >= 3 ? "Solid work! 💪" : "Every miss is a memory in the making. 🌱";
      var share = "I scored " + score + "/5 on today's Learning-Express Daily Quiz!";
      box.innerHTML = '<h2>' + score + " / " + qs.length + '</h2><p class="lead">' + msg + "</p>" +
        '<p>Turn today\'s misses into flashcards and review them tomorrow — that\'s spaced repetition in action.</p>' +
        '<div style="display:flex;gap:10px;flex-wrap:wrap"><button class="btn" id="qShare">Share score</button><a class="btn ghost" href="tools.html#flash">Make flashcards</a><a class="btn ghost" href="paths.html">Browse Express Lines</a></div>' +
        '<div class="card" style="margin-top:22px;background:var(--surface-2)"><h3>Get tomorrow\'s quiz + 5 free lessons weekly</h3><form class="form" id="qNl"><div class="row"><input type="email" name="email" placeholder="you@email.com" required aria-label="Email"><button class="btn signal" type="submit">Subscribe</button></div></form></div>';
      document.getElementById("qShare").onclick = function () { var u = location.href.split("#")[0]; if (navigator.share) navigator.share({ title: "Learning-Express Daily Quiz", text: share, url: u }).catch(function () {}); else { navigator.clipboard && navigator.clipboard.writeText(share + " " + u); LX.toast("Copied to clipboard!"); } };
      document.getElementById("qNl").onsubmit = function (e) { e.preventDefault(); var f = this; LX.submit("Newsletter signup (quiz)", { email: f.email.value, list: "Express Weekly", quiz_score: score + "/5" }).then(function () { f.innerHTML = '<p class="ok-msg">Subscribed! See you tomorrow.</p>'; LX.store.set("lead", true); }).catch(function () { LX.toast("Please try again."); }); };
    }
    q();
  }
})();
