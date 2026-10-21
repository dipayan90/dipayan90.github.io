// DOM-level test for the Q&A widget (docs/assets/javascripts/ask.js).
//
// Runs the shipped script against a minimal DOM stub so the search behaviour can be
// checked without a browser. Requires a built site: `mkdocs build` first.
//
// Usage: node scripts/test_ask.js

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const repo = path.join(__dirname, "..");
const scriptPath = path.join(repo, "docs", "assets", "javascripts", "ask.js");
const dataPath = path.join(repo, "site", "qa.json");

function makeElement(tag) {
  const element = {
    tagName: tag,
    children: [],
    className: "",
    href: "",
    value: "",
    hidden: false,
    listeners: {},
    appendChild(child) {
      this.children.push(child);
      return child;
    },
    addEventListener(name, handler) {
      (this.listeners[name] = this.listeners[name] || []).push(handler);
    },
    dispatch(name) {
      (this.listeners[name] || []).forEach((handler) => handler({ preventDefault() {} }));
    },
  };
  let text = "";
  Object.defineProperty(element, "textContent", {
    get() {
      return text !== "" ? text : this.children.map((child) => child.textContent).join("");
    },
    set(value) {
      text = String(value);
      if (value === "") {
        this.children = [];
      }
    },
  });
  return element;
}

const nodes = {};
for (const id of ["qa-widget", "qa-input", "qa-status", "qa-results", "qa-form", "qa-fallback"]) {
  nodes[id] = makeElement("div");
}
nodes["qa-widget"].hidden = true;

const requested = [];
global.document = {
  baseURI: "https://dipayan90.github.io/ask/",
  getElementById: (id) => nodes[id] || null,
  createElement: (tag) => makeElement(tag),
  createTextNode: (value) => ({ textContent: value, children: [] }),
};
global.document$ = { subscribe: (fn) => subscribers.push(fn) };
global.fetch = (url) => {
  requested.push(String(url));
  return Promise.resolve({
    ok: true,
    status: 200,
    json: () => Promise.resolve(JSON.parse(fs.readFileSync(dataPath, "utf8"))),
  });
};

const subscribers = [];
require(scriptPath);
assert.equal(subscribers.length, 1, "the widget registers exactly one navigation subscriber");

function waitFor(predicate) {
  return new Promise((resolve, reject) => {
    let waited = 0;
    const timer = setInterval(() => {
      if (predicate()) {
        clearInterval(timer);
        resolve();
      } else if ((waited += 10) > 2000) {
        clearInterval(timer);
        reject(new Error("timed out waiting for the widget to initialise"));
      }
    }, 10);
  });
}

function search(term) {
  nodes["qa-input"].value = term;
  nodes["qa-input"].dispatch("input");
  return nodes["qa-results"].children;
}

(async function run() {
  subscribers[0]();
  await waitFor(() => nodes["qa-widget"].hidden === false);

  assert.equal(requested[0], "https://dipayan90.github.io/qa.json", "fetches qa.json next to the page");
  assert.equal(nodes["qa-fallback"].hidden, true, "hides the no-JavaScript fallback");
  assert.match(nodes["qa-status"].textContent, /questions answered from this site/, "reports the corpus size");

  const hits = search("connect");
  assert.ok(hits.length >= 1, "a question about Connect returns at least one answer");
  assert.match(hits[0].textContent, /Amazon Connect/, "the best match mentions Amazon Connect");
  const link = hits[0].children[2].children[1];
  assert.equal(link.href, "../experience/", "the answer cites the page it came from");

  assert.equal(search("pods").length >= 1, true, "keyword matching finds team answers");
  assert.match(nodes["qa-status"].textContent, /answers? found/, "reports how many answers were found");

  search("zzzznotathing");
  assert.equal(nodes["qa-results"].children.length, 0, "a query with no match returns no results");
  assert.match(nodes["qa-status"].textContent, /No answer found/, "reports that nothing matched");

  search("");
  assert.equal(nodes["qa-results"].children.length, 0, "an empty query clears the results");

  const source = fs.readFileSync(scriptPath, "utf8");
  assert.ok(!source.includes("innerHTML"), "the widget never assigns innerHTML");

  console.log("test_ask: ok - widget fetches qa.json, ranks answers, hides the fallback and cites sources");
})().catch((error) => {
  console.error("test_ask: FAILED - " + error.message);
  process.exit(1);
});
