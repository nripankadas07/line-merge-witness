# Research — 21 October 2026

Demand is **inferred**, not a verified request for this tool. A merged-looking output can hide overlapping changes and make it difficult to locate the relevant base lines.

[Exact Most-stars search](https://github.com/search?q=three%20way%20merge&type=repositories&s=stars&o=desc), observed 2026-10-21T06:19:20.332Z. Highest-star relevant comparable found in the inspected pool: `git/git`. This is not an exhaustive global ranking.

| Comparable | Stars | Last push | License metadata | Observed workflow |
| --- | ---: | --- | --- | --- |
| [git/git](https://github.com/git/git) | 63923 | 2026-10-20T20:44:06Z | NOASSERTION | Version control and file merge with configurable conflict styles/algorithms. |
| [jj-vcs/jj](https://github.com/jj-vcs/jj) | 32176 | 2026-10-21T05:43:48Z | Apache-2.0 | Version-control system with conflict-aware history/workflows. |
| [libgit2/libgit2](https://github.com/libgit2/libgit2) | 10629 | 2026-10-16T14:02:20Z | NOASSERTION | Native C Git library; GPLv2 with linking exception described in README. |

## Choice and tradeoffs

Perform a read-only bounded three-way line merge with base-coordinate conflict regions and clean merged text. jsondiff and diffstat provide two-input structural/statistical comparisons. This implements a three-version base-relative line reconciliation algorithm with conflict components, not a wrapper.

The established alternatives are broader and often the better choice for their supported ecosystems. This tool provides one bounded inspectable report with an invented example and no runtime dependencies. READMEs/docs were read for install and example workflow; competitor clean install, time to first useful result, reliability, support response and performance were not measured. Own tests prove only the documented subset. Stars are research context, not performance or adoption evidence.

Keyword search coverage is narrow: Avro results include generators/profilers, event-time results include general streaming platforms, inventory-expiry results include unrelated homelab/certificate inventory, and three-way results include plugins and unrelated scraped text. Known relevant established tools were added directly. Spreadsheet comparison uses Excelize rather than an obsolete GitHub openpyxl mirror.

[Exact metadata and sampled current issues/PRs](RESEARCH_PROVENANCE.json). The samples are context, not verified competitor defects or requests for our new tool. Relevant Avro compatibility, POI SharedFormula and Git merge-file source was inspected; standard algorithms are original reimplementations. Microsoft CellFormula and Beam semantics informed the bounded contracts. No third-party code, branding or prose is copied.

Primary references:
- https://git-scm.com/docs/git-merge-file
