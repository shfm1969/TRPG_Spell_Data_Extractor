## Context

`parse_spell_data` in `app.py` parses the "成分" line of a spell block to populate five component columns. The current implementation only matches Chinese-character names. However, `需求說明.md` explicitly specifies that the Latin abbreviations V, S, M, F, DF must also be recognized. Spell documents sourced from English-translated rulebooks commonly list components as "成分：V, S, M" rather than writing out the full Chinese names.

## Goals / Non-Goals

**Goals:**
- Add V / S / M / F / DF letter-token detection to the existing component parsing block.
- Preserve all existing Chinese-character detection (no regressions).
- Handle the F vs DF ambiguity correctly (DF must not also trigger F).

**Non-Goals:**
- Changing any other parsing rule (casting time, range, duration, saving throw, spell resistance).
- Supporting mixed-case variants (v, s, m, f, df) — spec requires capital letters only.

## Decisions

### Decision: Use word-boundary-style regex for F vs DF disambiguation
The raw string may contain "DF" and we must not trigger the F rule in that case.

**Approach chosen**: After the component line is confirmed, check for `DF` first (set `[法器DF]`), then check for a standalone `F` that is not preceded by `D`. A simple approach: replace `DF` with a placeholder before checking `F`, or use regex `(?<!D)F(?![\w])`.

**Alternative considered**: Check order (check DF before F and skip F if DF matched) — simpler but fragile if a component line has both "F" and "DF" from two different segments.

**Chosen**: Use `re.search(r'(?<![A-Z])F(?![A-Z])', line)` to match a standalone F. This is robust and readable.

### Decision: Apply letter checks on the same line as Chinese checks (no separate branch)
Both Chinese-character and letter checks operate on the same "成分" line. They are additive — detecting "V" sets `[語言V]` regardless of whether "語言" is also present.

## Risks / Trade-offs

- **Risk**: A spell description body might accidentally contain a standalone "V", "S", or "M" that is not a component token.
  → **Mitigation**: The check only runs on lines that start with "成分", "法术成分", or "法術成分", so the scope is tightly bounded.

- **Risk**: DF/F regex slightly increases complexity.
  → **Mitigation**: One additional `re.search` call; negligible overhead.
