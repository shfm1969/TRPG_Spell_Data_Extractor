## Context

Two independent fixes share this change:

1. **Spec correction** — `openspec/specs/core.md` describes `[法抗]` using a length-based rule (`<= 5 chars → keep, else 其他`), but `app.py` has always used keyword-based logic (`不可` / `可`). A recent patch added "否" to the code without updating the spec. The spec simply needs to be rewritten to match reality.

2. **Verbose diagnostic flag** — When `--start-row 549 --batch-size 1` produces no updates and no error, developers have no way to know *why*: was the row filtered out? Did the heading match fail? Did the doc return empty text? Adding `--verbose` surfaces this information without changing production behavior.

## Goals / Non-Goals

**Goals:**
- Correct the `[法抗]` spec to reflect keyword-based mapping including "否".
- Add a `--verbose` CLI flag that emits per-row diagnostic lines to stdout.

**Non-Goals:**
- Changing any parsing logic — this is observability only.
- Fixing the actual root cause of the row-549 failure (unknown until verbose output is inspected).

## Decisions

### Decision: `--verbose` as an additive CLI flag (not a separate mode)
`--verbose` simply enables extra `print()` calls at key pipeline branch points. It does not change control flow or output format. This keeps the implementation trivial and reversible.

**Alternative considered**: A `--dry-run` flag that also skips writes. Deferred — orthogonal concern.

### Decision: Diagnostic print points
Four locations emit verbose output when `--verbose` is set:
1. `filter_rows_for_processing` — per row: "Row N: skipped (no URL / URL invalid / all fields filled)" or "Row N: queued for processing"
2. `parse_spell_data` entry — `target_name` derived from `spell_name`
3. Heading match result — matched line + line index, or "no heading match → skipping"
4. `parse_spell_data` return — dict of extracted fields (or empty)

A single `verbose: bool` parameter is threaded through the relevant functions.

## Risks / Trade-offs

- **Risk**: Verbose output may be noisy in batch runs.
  → **Mitigation**: Flag is opt-in; default is silent.
- **Risk**: Passing `verbose` through function signatures slightly widens the API surface.
  → **Mitigation**: Functions are script-internal; no public API concerns.
