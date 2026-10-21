# FACTS.md — canonical fact sheet for dipayan90.github.io

Single source of truth for every public claim on the site. Every page, and every
artifact generated later (`llms.txt`, `profile.json`, JSON-LD, the Q&A corpus),
must trace back to a line in this file.

**Provenance rule.** Each claim is attributed to one of:

- `LinkedIn (canonical)` — from the owner's current LinkedIn profile export
  ("Profile (4).pdf", uploaded on KAJ-9; extracted text held as the
  `linkedin-profile-source` document on KAJ-9). Where the site and this profile
  disagree, the profile wins.
- `site (owner-authored)` — a claim that appears on the pre-existing site and is
  not in the LinkedIn profile. It is kept, but marked here so later generation
  does not silently drop or re-assert it.

No claim may be added to the site without a supporting line below. If a claim
cannot be sourced, it is removed or softened.

**Last reviewed:** 2026-10. Every page carries a matching `*Last reviewed: 2026-10*`
line at the end.

---

## Identity

| Field | Value | Source |
|---|---|---|
| Name | Dipayan Chattopadhyay | LinkedIn (canonical) |
| Current role | Software Development Manager | LinkedIn (canonical) |
| Current company | Amazon Web Services (AWS) | LinkedIn (canonical) |
| Location | Greater Seattle Area, Washington, United States | LinkedIn (canonical) |
| Summary | Results-driven software engineering leader with over 10 years of experience leading large-scale distributed systems, driving organizational transformation, and delivering customer-obsessed innovation | LinkedIn (canonical) |
| Email | dipayan90@gmail.com | LinkedIn (canonical) |
| LinkedIn | https://www.linkedin.com/in/dchattopadhyay | LinkedIn (canonical) |
| Blog | https://dipayan90.wordpress.com | LinkedIn (canonical) |
| GitHub | https://github.com/dipayan90 | LinkedIn (canonical) |
| Personal site | https://dipayan90.github.io | LinkedIn (canonical) |

## Experience timeline

All entries carry month-year dates. Source: LinkedIn (canonical).

| Company | Title | Start | End | Location |
|---|---|---|---|---|
| Amazon Web Services | Software Development Manager | September 2023 | Present | Greater Seattle Area |
| Amazon Web Services | Senior Software Engineer | June 2022 | September 2023 | Greater Seattle Area |
| Amazon (AWS) | Software Engineer | January 2020 | June 2022 | Greater Seattle Area |
| Nordstrom | Senior Engineer – ML Platform | November 2018 | January 2020 | Greater Seattle Area |
| Nordstrom | Senior Engineer | February 2018 | November 2018 | Greater Seattle Area |
| Nordstrom | Engineer 2 | February 2017 | February 2018 | Greater Seattle Area |
| CDK Global | Software Engineer 2 | July 2015 | February 2017 | Greater Seattle Area |
| CDK Global | Software Engineer 1 | August 2014 | June 2015 | Greater Seattle Area |
| University of Cincinnati | Teaching Assistant | January 2014 | May 2014 | Cincinnati |
| UPS Supply Chain Solutions | Software Development Intern | August 2013 | January 2014 | Alpharetta, GA |
| University of Cincinnati | Technical Consultant | February 2013 | June 2013 | Cincinnati |
| University of Cincinnati | Teaching Assistant | August 2012 | February 2013 | Cincinnati |
| RCI | Intern | March 2010 | May 2010 | Greater Hyderabad Area |
| CMC Ltd | Intern | March 2009 | May 2009 | Greater Hyderabad Area |

**Omitted from the site (retained here for completeness):** the University of
Cincinnati 2014 TA stint, the 2012–2013 UC TA stint, the UC Technical Consultant
stint, and the RCI and CMC Ltd internships are low-signal for a portfolio; they
are recorded here and not listed on `experience.md`. Site claims of "over 10
years" reflect the January 2020 start of full-time professional work plus the
internship history and an overall career spanning 2014–present.

## Education

| Degree | Institution | Years | Source |
|---|---|---|---|
| Master of Science, Computer Science | University of Cincinnati | 2012 – 2014 | LinkedIn (canonical) |
| Bachelor of Technology, Computer Science | SRM University | 2008 – 2012 | LinkedIn (canonical) |

**Removed claim:** the earlier site stated a master's thesis, "Data Mining
Techniques for Pattern Recognition in Large Datasets", dated 2011–2013. The
LinkedIn profile lists no thesis and gives 2012–2014. The fabricated thesis and
the wrong dates were removed. `site (owner-authored, unverified)`.

## Skills

### Top skills (LinkedIn "Top Skills")

- Artificial Intelligence (AI) — `LinkedIn (canonical)`
- Engineering Management — `LinkedIn (canonical)`
- Systems Development Management — `LinkedIn (canonical)`

### Technical stack on the site

The `skills.md` inventory (programming-language proficiency bars and technology
tags: Java, Python, JavaScript, Scala; Spring, Node, Angular; AWS services;
Docker, Kubernetes; MongoDB, Redis; Apache Spark, Hive, NiFi, Airflow; Kafka,
ActiveMQ, RabbitMQ) is `site (owner-authored)`. It is consistent with the
technologies named in the LinkedIn roles but the specific proficiency ordering is
the owner's own presentation, not a LinkedIn claim.

## Languages

| Language | Proficiency | Source |
|---|---|---|
| Telugu | Native or Bilingual | LinkedIn (canonical) |
| Bengali | Native or Bilingual | LinkedIn (canonical) |
| English | Full Professional | LinkedIn (canonical) |
| Hindi | Full Professional | LinkedIn (canonical) |
| Tamil | Elementary | LinkedIn (canonical) |
| Japanese | Elementary | LinkedIn (canonical) |

The site previously said "5 languages fluently". Corrected to **6 languages**,
at levels from native fluency to elementary. `LinkedIn (canonical)`.

## Honors & Awards

- University Graduate Scholarship — `LinkedIn (canonical)`
- Outstanding Student Award — `LinkedIn (canonical)`

## Named projects / systems

| Project | Link | Status | Source |
|---|---|---|---|
| Spring Actuator CloudWatch | https://github.com/dipayan90/spring-actuator-cloudwatch | Live (HTTP 200) | site (owner-authored) |
| Big-data Profiler | https://github.com/Nordstrom/bigdata-profiler | **Dead (HTTP 404)** — link repointed to https://github.com/dipayan90 | site (owner-authored) |
| Deep Learning Image Similarity | https://github.com/dipayan90/deep-learning-image-similarity | Live (HTTP 200) | site (owner-authored) |
| Autoerroretry | https://github.com/dipayan90/autoerroretry | Live (HTTP 200) | site (owner-authored) |
| Time-Series Anomaly Detection (anomaly-detect-core) | https://github.com/dipayan90/anomaly-detect-core | Live (HTTP 200) | site (owner-authored) |
| Conference talk: "Building an ML Platform at Scale" | https://www.youtube.com/watch?v=F8C58OZW3-M | Live (HTTP 200) | site (owner-authored) |

The five project cards on `opensource.md` are the site's public project list;
they are not enumerated on the LinkedIn profile. The dead "Stars"/"Forks" stat
placeholders on each card were removed — no static source can verify counts, and
the numbers were never populated.

## Quantified claims

Every number asserted on the site, with its source. All LinkedIn items are from
the AWS Software Development Manager role (September 2023 – Present) unless noted.

| Claim | Value | Source |
|---|---|---|
| Years of experience | over 10 years | LinkedIn (canonical) |
| Engineers managed | 20 engineers across 4 pods | LinkedIn (canonical) |
| Onboarding time reduction | 50% | LinkedIn (canonical) |
| Test coverage improvement | 60% → 90% | LinkedIn (canonical) |
| Engineers promoted into leadership | 4 | LinkedIn (canonical) |
| Team retention | 90% | LinkedIn (canonical) |
| Partner teams in cross-org initiatives | 5+ | LinkedIn (canonical) |
| Production incident reduction | 40% | LinkedIn (canonical) |
| System reliability | 99.99% | LinkedIn (canonical) |
| Operational readiness reviews bar-raised | 20+ | LinkedIn (canonical) |
| Contacts handled by Amazon Connect orchestration platform | ~40 million / month | LinkedIn (canonical) |
| Car dealerships served by CDK social products | 26,000+ | LinkedIn (canonical) |
| Major platforms built | 3 | site (owner-authored) |
| Open source projects | 5 | site (owner-authored, matches the five project cards) |
| "Multilingual (5 languages)" | **was wrong** → 6 languages | LinkedIn (canonical) |

## Site facts

- **Sections and pages:** Home `docs/index.md`; About Me `docs/summary.md`;
  Experience `docs/experience.md`; Projects `docs/opensource.md`; Skills &
  Expertise `docs/skills.md`; Personal `docs/miscellaneous.md`.
- **Footer year:** the copyright year is rendered at build time from the MkDocs
  build clock, not hard-coded. `mkdocs.yml` sets
  `copyright: Copyright &copy; Dipayan Chattopadhyay` (no year), and
  `overrides/partials/copyright.html` injects `build_date_utc.year`. The footer
  therefore cannot go stale. `site (owner-authored)`.
- **`last_reviewed` policy:** every page ends with `*Last reviewed: 2026-10*`.
  The freshness guard (a later task) checks these dates.
- **Hosting:** MkDocs Material, GitHub Pages, static output only — no backend, no
  runtime model calls, no paid services. Owner-decided constraints.

## Link audit

Checked 2026-10-21 with `curl -sIL` (HTTP status):

| Link | Status | Action |
|---|---|---|
| https://github.com/dipayan90/spring-actuator-cloudwatch | 200 | OK |
| https://github.com/Nordstrom/bigdata-profiler | 404 | **Dead** — repointed card link to https://github.com/dipayan90 |
| https://github.com/dipayan90/deep-learning-image-similarity | 200 | OK |
| https://github.com/dipayan90/autoerroretry | 200 | OK |
| https://github.com/dipayan90/anomaly-detect-core | 200 | OK |
| https://www.youtube.com/watch?v=F8C58OZW3-M | 200 | OK |
| https://dipayan90.wordpress.com | 200 | OK (also 200 over http; site now uses https) |
| https://github.com/dipayan90 | 200 | OK |
| https://drive.google.com/file/d/1laT67xxMLH0JHuavO3VTqt0qcclG4BIU/view | 404 | **Dead** — CV button removed (see Decisions) |
| https://www.linkedin.com/in/dchattopadhyay | 999 | Bot-block; treated as live (owner's canonical profile) |

## Decisions

### CV link — removed, replaced with LinkedIn

The Home hero had a "Download CV" button pointing at a Google Drive file
(`1laT67xxMLH0JHuavO3VTqt0qcclG4BIU`). That URL returns **HTTP 404** — the file
is gone or no longer public. Two options were considered: host the CV in-repo, or
remove the link.

**Decision: remove the link.** No retrievable CV artifact exists to host, and the
zero-cost / no-new-infrastructure constraint plus the content-truth rule argue
against shipping a stale or fabricated CV. The hero CTA row now keeps the
"Explore Portfolio" button and adds a "LinkedIn" button to
https://www.linkedin.com/in/dchattopadhyay, the owner's canonical, always-current
professional profile. If the owner later supplies a real CV file, it can be added
under `docs/assets/` and the button restored.

### Removed unsupported superlative

`experience.md` described a CDK Global promotion as "in a record 11 months—faster
than any peer in a similar role". The superlative is unsupported by LinkedIn.
Replaced with a factual statement: promoted after 11 months, with responsibility
for nine state and federal carrier integrations at nationwide scale.

---

*Last reviewed: 2026-10*
