## Why

Two bugs exist: (1) The `[法抗]` specification describes a length-based rule but the code implements keyword-based logic (不可/可/否/其他), and the recently added "否" value is entirely undocumented in the spec. (2) Running `--start-row 549` produces no updates for 9 expected fields, but there is no diagnostic output to identify which pipeline stage fails (filter, heading match, or field parsing).

## What Changes

- **Spec correction**: Update the `core` spec's `[法抗]` requirement to reflect keyword-based mapping (不可 / 可 / 否 / 其他) instead of the incorrect length-based description.
- **Add `--verbose` flag**: When passed, the script prints per-row diagnostics:
  - Whether the row passed the filter (and why it was skipped if not)
  - The `search_name` and derived `target_name` used for heading matching
  - Whether the heading match succeeded, and which line matched
  - Which fields were extracted from the doc
- This allows immediate diagnosis of the row-549 failure without guessing.

## Capabilities

### New Capabilities
- (none)

### Modified Capabilities
- `core`: The `[法抗]` (Spell Resistance) requirement description is wrong — replace with accurate keyword-based spec including "否".

## Impact

- `app.py` — `main()` for argument parsing; `filter_rows_for_processing`, `parse_spell_data` for verbose output.
- `openspec/specs/core.md` — `[法抗]` requirement corrected.
- No new dependencies.
