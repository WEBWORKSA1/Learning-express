/* Learning-Express study tools */
(function () {
  var LX = window.LX, $ = function (s) { return document.querySelector(s); }, esc = LX.esc, store = LX.store;

  // tabs + hash routing
  function show(id) {
    document.querySelectorAll(".tool").forEach(function (t) { t.classList.toggle("on", t.id === "t-" + id); });
    document.querySelectorAll("[data-tool]").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-tool") === id ? "true" : "false"); });
  }
  document.querySelectorAll("[data-tool]").forEach(function (b) { b.addEventListener("click", function () { show(b.getAttribute("data-tool")); history.replaceState(null, "", "#" + b.getAttribute("data-tool")); }); });
  var h = location.hash.slice(1); if (h && document.getElementById("t-" + h)) show(h);

  // ---------- flashcards
  var deck = store.get("deck", []), i = 0, known = 0;
  var card = $("#fcCard"), front = $("#fcFront"), back = $("#fcBack"), stat = $("#fcStat"), input = $("#fcInput");
  var SAMPLE = "Active recall :: Retrieving information from memory instead of re-reading it\nSpaced repetition :: Reviewing at expanding intervals just before you'd forget\nFeynman technique :: Explaining a concept simply to find gaps\nPomodoro :: 25-minute focused sprint followed by a 5-minute break\nInterleaving :: Mixing different topics or problem types in one session\nCompound interest :: Interest earned on both principal and past interest";
  function parse(t) { return t.split("\n").map(function (l) { var p = l.split("::"); return p.length > 1 ? { q: p[0].trim(), a: p.slice(1).join("::").trim() } : null; }).filter(Boolean); }
  function draw() {
    if (!deck.length) { front.textContent = "Load a deck to begin"; back.textContent = ""; return; }
    card.classList.remove("flip");
    var c = deck[i % deck.length]; front.textContent = c.q; setTimeout(function () { back.textContent = c.a; }, 150);
    stat.textContent = "Card " + ((i % deck.length) + 1) + " of " + deck.length + " · Known this round: " + known;
  }
  if (input && deck.length) input.value = deck.map(function (c) { return c.q + " :: " + c.a; }).join("\n");
  $("#fcLoad").onclick = function () { deck = parse(input.value); store.set("deck", deck); i = 0; known = 0; draw(); LX.toast(deck.length + " cards loaded"); };
  $("#fcSample").onclick = function () { input.value = SAMPLE; $("#fcLoad").onclick(); };
  $("#fcShuffle").onclick = function () { deck.sort(function () { return Math.random() - .5; }); i = 0; draw(); };
  card.onclick = function () { card.classList.toggle("flip"); };
  card.onkeydown = function (e) { if (e.key === " " || e.key === "Enter") { e.preventDefault(); card.classList.toggle("flip"); } };
  $("#fcKnow").onclick = function () { if (!deck.length) return; known++; deck.splice(i % deck.length, 1); store.set("deck", deck); if (!deck.length) { front.textContent = "🎉 Deck complete! Reload to review again."; stat.textContent = ""; return; } draw(); };
  $("#fcAgain").onclick = function () { if (!deck.length) return; i++; draw(); };
  draw();

  // ---------- timer
  var mins = 25, left = 25 * 60, tick = null, disp = $("#tmDisplay"), lbl = $("#tmLabel");
  var today = new Date().toISOString().slice(0, 10), cnt = store.get("sprints", { d: today, n: 0 }); if (cnt.d !== today) cnt = { d: today, n: 0 };
  $("#tmCount").textContent = cnt.n;
  function paint() { var m = Math.floor(left / 60), s = left % 60; disp.textContent = (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s; document.title = disp.textContent + " · Focus Timer"; }
  function beep() { try { var a = new (window.AudioContext || window.webkitAudioContext)(), o = a.createOscillator(); o.frequency.value = 880; o.connect(a.destination); o.start(); setTimeout(function () { o.stop(); }, 400); } catch (e) {} }
  $("#tmStart").onclick = function () {
    if (tick) { clearInterval(tick); tick = null; this.textContent = "Resume"; return; }
    this.textContent = "Pause";
    tick = setInterval(function () {
      left--; paint();
      if (left <= 0) { clearInterval(tick); tick = null; beep(); $("#tmStart").textContent = "Start";
        if (mins >= 25) { cnt.n++; store.set("sprints", cnt); $("#tmCount").textContent = cnt.n; LX.toast("Sprint complete! Take a break."); } else LX.toast("Break over — back to it!");
        left = mins * 60; paint(); }
    }, 1000);
  };
  $("#tmReset").onclick = function () { clearInterval(tick); tick = null; left = mins * 60; paint(); $("#tmStart").textContent = "Start"; };
  document.querySelectorAll("[data-mins]").forEach(function (b) { b.onclick = function () {
    document.querySelectorAll("[data-mins]").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
    mins = +b.getAttribute("data-mins"); lbl.textContent = mins >= 25 ? "Focus sprint" : "Break"; $("#tmReset").onclick(); }; });
  paint();

  // ---------- spaced review scheduler
  var spDate = $("#spDate"); spDate.value = today;
  $("#spGo").onclick = function () {
    var t = $("#spTopic").value || "Your topic", d0 = new Date(spDate.value + "T12:00:00");
    var rows = [1, 3, 7, 14, 30].map(function (n, k) { var d = new Date(d0.getTime() + n * 864e5); return "<tr><td>Review " + (k + 1) + "</td><td>Day " + n + "</td><td><strong>" + d.toLocaleDateString("en", { weekday: "short", month: "short", day: "numeric" }) + "</strong></td></tr>"; }).join("");
    var ics = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Learning-Express//Review//EN\n" + [1, 3, 7, 14, 30].map(function (n) { var d = new Date(d0.getTime() + n * 864e5).toISOString().slice(0, 10).replace(/-/g, ""); return "BEGIN:VEVENT\nUID:" + d + n + "@learning-express\nDTSTAMP:" + d + "T090000Z\nDTSTART;VALUE=DATE:" + d + "\nSUMMARY:Review: " + t.replace(/[,;\n]/g, " ") + "\nEND:VEVENT"; }).join("\n") + "\nEND:VCALENDAR";
    $("#spOut").innerHTML = "<h3>" + esc(t) + '</h3><table class="t"><tbody>' + rows + '</tbody></table><p style="margin-top:12px"><a class="btn sm ghost" download="review-schedule.ics" href="data:text/calendar;charset=utf-8,' + encodeURIComponent(ics) + '">📅 Add to calendar (.ics)</a></p>';
  };

  // ---------- GPA
  var GR = { "A+": 4, "A": 4, "A-": 3.7, "B+": 3.3, "B": 3, "B-": 2.7, "C+": 2.3, "C": 2, "C-": 1.7, "D+": 1.3, "D": 1, "F": 0 };
  var tb = document.querySelector("#gpaTable tbody");
  function row(n, c, g) {
    var tr = document.createElement("tr");
    tr.innerHTML = '<td><input value="' + esc(n || "") + '" placeholder="Course" aria-label="Course"></td><td><input type="number" value="' + (c || 3) + '" min="0" step="0.5" aria-label="Credits" style="max-width:90px"></td><td><select aria-label="Grade">' + Object.keys(GR).map(function (k) { return "<option" + (k === (g || "A") ? " selected" : "") + ">" + k + "</option>"; }).join("") + '</select></td><td><button class="icon-btn" aria-label="Remove">✕</button></td>';
    tr.querySelector("button").onclick = function () { tr.remove(); calc(); };
    tr.addEventListener("input", calc); tb.appendChild(tr);
  }
  function calc() { var pts = 0, cr = 0; tb.querySelectorAll("tr").forEach(function (tr) { var c = parseFloat(tr.querySelectorAll("input")[1].value) || 0, g = GR[tr.querySelector("select").value]; pts += c * g; cr += c; }); $("#gpaOut").textContent = cr ? (pts / cr).toFixed(2) : "0.00"; $("#gpaCred").textContent = "(" + cr + " credits)"; }
  row("Biology", 3, "A-"); row("Statistics", 4, "B+"); row("English", 3, "A"); calc();
  $("#gpaAdd").onclick = function () { row("", 3, "B"); calc(); };

  // ---------- final grade needed
  function fg() { var c = +$("#fgCur").value, w = +$("#fgWant").value, p = +$("#fgW").value / 100; var need = (w - c * (1 - p)) / p;
    $("#fgOut").innerHTML = isFinite(need) ? (need > 100 ? "You'd need <strong>" + need.toFixed(1) + "%</strong> — above 100%, so consider extra credit or adjusting your target." : need <= 0 ? "You've already secured it — anything on the final works! 🎉" : "You need <strong>" + need.toFixed(1) + "%</strong> on the final exam.") : ""; }
  ["#fgCur", "#fgWant", "#fgW"].forEach(function (s) { $(s).addEventListener("input", fg); }); fg();

  // ---------- reading speed
  var PASS = "Learning is not a spectator sport. Research on memory consistently shows that people remember more when they actively retrieve information than when they simply reread it. That is why self-testing, flashcards and practice questions are so effective. Spacing study sessions over several days also helps, because each review strengthens memory just as it begins to fade. Sleep plays a role too: during rest, the brain consolidates what was learned during the day. Put together, these findings suggest a simple recipe. Study in focused sessions, test yourself instead of rereading, review on a schedule, and protect your sleep. None of these strategies require expensive tools or special talent. They require only a plan and the willingness to make learning feel a little harder in the moment so that it lasts much longer.";
  var rt0 = 0;
  $("#rdStart").onclick = function () { $("#rdText").style.display = "block"; $("#rdText").textContent = PASS; rt0 = Date.now(); this.disabled = true; $("#rdDone").disabled = false; $("#rdOut").textContent = ""; };
  $("#rdDone").onclick = function () { var sec = (Date.now() - rt0) / 1000, wpm = Math.round(PASS.split(/\s+/).length / (sec / 60)); $("#rdOut").innerHTML = "<strong>" + wpm + " words per minute.</strong> " + (wpm < 200 ? "Below average adult pace — practise with easy material." : wpm < 300 ? "Typical adult reading speed." : "Faster than average — check comprehension too!"); this.disabled = true; $("#rdStart").disabled = false; $("#rdStart").textContent = "Try again"; };

  // ---------- typing
  var TX = ["The quick brown fox jumps over the lazy dog while learners practise every single day.", "Small habits repeated daily become the skills that change careers and lives.", "Focus on one station at a time and the whole line will take care of itself.", "Practice testing and spaced review beat rereading for long term memory."];
  var target = "", tStart = 0, tTimer = null;
  function tyReset() { target = TX.concat(TX).sort(function () { return Math.random() - .5; }).join(" "); $("#tyText").textContent = target; $("#tyIn").value = ""; $("#tyIn").disabled = false; clearInterval(tTimer); tTimer = null; tStart = 0; $("#tyTime").textContent = 60; $("#tyWpm").textContent = 0; $("#tyAcc").textContent = 100; }
  $("#tyIn").addEventListener("input", function () {
    var v = this.value;
    if (!tStart) { tStart = Date.now(); tTimer = setInterval(function () { var l = 60 - Math.floor((Date.now() - tStart) / 1000); $("#tyTime").textContent = Math.max(0, l); if (l <= 0) { clearInterval(tTimer); $("#tyIn").disabled = true; LX.toast("Time! " + $("#tyWpm").textContent + " WPM"); } }, 250); }
    var ok = 0, html = ""; for (var k = 0; k < target.length; k++) { if (k < v.length) { var good = v[k] === target[k]; if (good) ok++; html += '<span class="' + (good ? "ok" : "bad") + '">' + esc(target[k]) + "</span>"; } else html += esc(target[k]); }
    $("#tyText").innerHTML = html;
    var mins = Math.max((Date.now() - tStart) / 60000, 1 / 60); $("#tyWpm").textContent = Math.round(ok / 5 / mins); $("#tyAcc").textContent = v.length ? Math.round(ok / v.length * 100) : 100;
  });
  $("#tyReset").onclick = tyReset; tyReset();

  // ---------- goal hours
  function gh() { var n = +$("#ghNeed").value, w = +$("#ghWeek").value; if (!n || !w) return; var wk = n / w, d = new Date(Date.now() + wk * 7 * 864e5);
    $("#ghOut").innerHTML = "About <strong>" + Math.ceil(wk) + " weeks</strong> — you could finish by <strong>" + d.toLocaleDateString("en", { month: "long", day: "numeric", year: "numeric" }) + "</strong>."; }
  ["#ghNeed", "#ghWeek"].forEach(function (s) { $(s).addEventListener("input", gh); }); gh();
})();
