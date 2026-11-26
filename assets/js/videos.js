/* Video Express: renders auto-updated lessons from data/videos.json */
(function () {
  var LX = window.LX || {}, esc = LX.esc || function (s) { return s; };
  function fmt(d) { try { return new Date(d).toLocaleDateString("en", { month: "short", day: "numeric", year: "numeric" }); } catch (e) { return ""; } }
  function card(v) {
    return '<div class="card vcard">' + LX.vidHTML(v) + "<h3>" + esc(v.title) + '</h3><div class="meta"><span>' + esc(v.channel) + "</span><span>" + fmt(v.date) + "</span></div></div>";
  }
  fetch("data/videos.json", { cache: "no-cache" }).then(function (r) { return r.json(); }).then(function (data) {
    var items = data.items || [];
    // Line pages
    document.querySelectorAll("[data-line-videos]").forEach(function (box) {
      var cat = box.getAttribute("data-line-videos");
      var list = items.filter(function (v) { return (v.cats || []).indexOf(cat) > -1; }).slice(0, 4);
      box.innerHTML = list.length ? list.map(card).join("") : '<p class="note">New lessons for this line are loading in the next daily refresh.</p>';
    });
    var hv = document.getElementById("homeVideos");
    if (hv && !hv.querySelector(".vcard") && items.length) hv.innerHTML = items.slice(0, 6).map(card).join("");
    // Library page
    var grid = document.getElementById("vgrid");
    if (!grid) return;
    var cat = "all", q = "", shown = 12;
    function filtered() {
      return items.filter(function (v) {
        return (cat === "all" || (v.cats || []).indexOf(cat) > -1) && (!q || (v.title + " " + v.channel).toLowerCase().indexOf(q) > -1);
      });
    }
    function render() {
      var f = filtered();
      grid.innerHTML = f.slice(0, shown).map(card).join("") || '<p class="note">No videos match — try another topic.</p>';
      var more = document.getElementById("vmore"); if (more) more.style.display = f.length > shown ? "" : "none";
    }
    document.getElementById("vchips").addEventListener("click", function (e) {
      var b = e.target.closest(".chip"); if (!b) return;
      document.querySelectorAll("#vchips .chip").forEach(function (c) { c.setAttribute("aria-pressed", c === b ? "true" : "false"); });
      cat = b.getAttribute("data-cat"); shown = 12; render();
    });
    var vq = document.getElementById("vq"); if (vq) vq.addEventListener("input", function () { q = vq.value.trim().toLowerCase(); shown = 12; render(); });
    var more = document.getElementById("vmore"); if (more) more.addEventListener("click", function () { shown += 12; render(); });
    render();
    var ch = document.getElementById("vchan");
    if (ch) ch.innerHTML = (data.channels || []).filter(function (c) { return c.ok; }).map(function (c) {
      return '<a class="card" href="https://www.youtube.com/channel/' + esc(c.id) + '" target="_blank" rel="noopener"><h3 style="font-size:1rem">' + esc(c.name) + ' ↗</h3><p class="note mb0">' + esc((c.cats || []).join(" · ")) + "</p></a>";
    }).join("");
  }).catch(function () {});
})();
