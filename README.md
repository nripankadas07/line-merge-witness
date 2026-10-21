# line-merge-witness

Perform a read-only bounded three-way line merge with base-coordinate conflict regions and clean merged text.

For configuration reviewers comparing two text edits with their common base.

## Quickstart

Python3.10+; no external service or runtime dependencies. Linux shell:

```sh
git clone https://github.com/nripankadas07/line-merge-witness.git
cd line-merge-witness
python -m venv .venv
. .venv/bin/activate
python -m pip install .
line-merge-witness base.txt left.txt right.txt
```

The invented three files merge independent first/last line changes cleanly. [Expected JSON](example-output.json).

## Input and interpretation

Arguments are BASE LEFT RIGHT. The three files are read only. [base.txt](base.txt), [left.txt](left.txt) and [right.txt](right.txt) are invented fixtures.

Three UTF-8 files, each<=1MiB and500 Python splitlines(keepends=True) lines. Original deterministic quadratic LCS; ties prefer deleting from base. Cross-side nonempty edit intervals overlap only in their interiors; insertion overlaps a replacement only strictly inside it; two insertions overlap at the same point. Boundary insertions remain independent, identical alternatives coalesce. Transitive overlap components conservatively conflict when materialized alternatives differ. Base coordinates zero-based half-open. Any conflict sets merged_text=null; report preserves alternatives. CRLF and final-newline differences are significant. No Git invocation, rename/directory/binary/semantic merge or promise to match Git alignment/conflict decisions.

Exit0: completed result without a finding/conflict; exit1: documented schema/shared-formula/stockout finding or merge conflict; exit2: malformed/unsupported input, stderr and no partial JSON report. Event-time drops are normal policy decisions and use exit0. A completed report is evidence only about the supplied model and supported subset. No automatic live-system changes.

## Verification

```sh
python -m unittest -v
python -m compileall -q line_merge_witness.py
python -m pip wheel --no-deps . -w dist
```

225 small-sequence LCS reconstructions and675 single/identical-side merge checks,125 side-swap cases, conflicts/adjacent edits/interior/boundary insertions, CRLF/EOF and line bound. [Validation record](VALIDATION.md). CI checks Python3.10/3.12/3.14 and a wheel-installed console from outside the checkout. Windows/macOS and production-size workloads are not verified. No benchmark or superiority claim.

## Scope and provenance

Alpha utility, original AI-assisted implementation and invented fixtures. Standard algorithms were reimplemented; no third-party implementation/prose copied. MIT. [Candidate brief](BRIEF.json), [dated research and alternatives](RESEARCH.md), [support](SUPPORT.md), [contribution guide](CONTRIBUTING.md), [security](SECURITY.md).

jsondiff and diffstat provide two-input structural/statistical comparisons. This implements a three-version base-relative line reconciliation algorithm with conflict components, not a wrapper.
