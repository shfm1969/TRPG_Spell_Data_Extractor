## 1. Extend Component Parsing in app.py

- [x] 1.1 Add `import re` guard at top of component block (already imported at module level — verify no duplication)
- [x] 1.2 In the `parse_spell_data` component parsing block, add V-token detection: if `re.search(r'\bV\b', line)` → set `[語言V]` = "語"
- [x] 1.3 Add S-token detection: if `re.search(r'\bS\b', line)` → set `[姿勢S]` = "姿"
- [x] 1.4 Add M-token detection: if `re.search(r'\bM\b', line)` → set `[材料M]` = "材"
- [x] 1.5 Add DF-token detection (before F check): if `re.search(r'\bDF\b', line)` → set `[法器DF]` = "法"
- [x] 1.6 Add standalone F-token detection (after DF check): if `re.search(r'(?<![A-Z])F(?![A-Z])', line)` → set `[器材F]` = "器"

## 2. Verification

- [x] 2.1 Manual test: run `uv run app.py --start-row <row>` on a spell whose Doc uses "成分：V, S, M" and confirm the three columns are filled
- [x] 2.2 Manual test: run on a spell whose Doc uses "成分：DF, S" and confirm `[法器DF]` = "法", `[姿勢S]` = "姿", `[器材F]` remains empty
- [x] 2.3 Confirm existing Chinese-character spells are unaffected (no regression)
