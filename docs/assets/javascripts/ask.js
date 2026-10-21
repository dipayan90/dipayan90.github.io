(function () {
  "use strict";

  var DATA_URL = "../qa.json";

  function score(entry, terms) {
    var q = entry.q.toLowerCase();
    var a = entry.a.toLowerCase();
    var kw = entry.keywords.join(" ").toLowerCase();
    var total = 0;
    terms.forEach(function (term) {
      if (q.indexOf(term) !== -1) { total += 3; }
      if (kw.indexOf(term) !== -1) { total += 2; }
      if (a.indexOf(term) !== -1) { total += 1; }
    });
    return total;
  }

  function render(list, entries, terms) {
    list.textContent = "";
    entries
      .map(function (entry) { return { entry: entry, hits: score(entry, terms) }; })
      .filter(function (hit) { return hit.hits > 0; })
      .sort(function (a, b) { return b.hits - a.hits; })
      .forEach(function (hit) {
        var item = document.createElement("li");
        var question = document.createElement("p");
        var answer = document.createElement("p");
        var source = document.createElement("p");
        var link = document.createElement("a");
        question.className = "qa-r-q";
        answer.className = "qa-r-a";
        source.className = "qa-r-source";
        question.textContent = hit.entry.q;
        answer.textContent = hit.entry.a;
        link.href = hit.entry.sourceUrl;
        link.textContent = hit.entry.sourceLabel;
        source.appendChild(document.createTextNode("Source: "));
        source.appendChild(link);
        item.appendChild(question);
        item.appendChild(answer);
        item.appendChild(source);
        list.appendChild(item);
      });
  }

  function init() {
    var widget = document.getElementById("qa-widget");
    if (!widget) { return; }
    var input = document.getElementById("qa-input");
    var status = document.getElementById("qa-status");
    var list = document.getElementById("qa-results");
    var fallback = document.getElementById("qa-fallback");

    fetch(new URL(DATA_URL, document.baseURI)).then(function (response) {
      if (!response.ok) { throw new Error("HTTP " + response.status); }
      return response.json();
    }).then(function (data) {
      var entries = data.entries;
      widget.hidden = false;
      if (fallback) { fallback.hidden = true; }
      function update() {
        var terms = input.value.toLowerCase().split(/\s+/).filter(Boolean);
        if (!terms.length) { status.textContent = ""; list.textContent = ""; return; }
        render(list, entries, terms);
        var found = list.children.length;
        status.textContent = found
          ? found + (found === 1 ? " answer" : " answers") + " found."
          : "No answer found. Try different words.";
      }
      input.addEventListener("input", update);
      document.getElementById("qa-form").addEventListener("submit", function (event) {
        event.preventDefault();
        update();
      });
      status.textContent = entries.length + " questions answered from this site.";
    }).catch(function () {
      status.textContent = "";
    });
  }

  if (typeof document$ !== "undefined") { document$.subscribe(init); }
  else { document.addEventListener("DOMContentLoaded", init); }
})();
