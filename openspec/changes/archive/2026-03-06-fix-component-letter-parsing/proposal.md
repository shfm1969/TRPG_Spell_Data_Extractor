## Why

The component parsing logic in `parse_spell_data` only recognizes Chinese-character component names (語言、姿勢、材料、器材、法器), but spell documents often list components using the standard letter abbreviations (V, S, M, F, DF). This causes the five component columns to remain empty for any spell whose source document uses letter-based notation.

## What Changes

- Extend the component parsing block in `parse_spell_data` to also detect V / S / M / F / DF letter tokens on the "成分" line, in addition to the existing Chinese-character detection.
- Detection rules (matching `需求說明.md`):
  - `V` present → `[語言V]` = "語"
  - `S` present → `[姿勢S]` = "姿"
  - `M` present → `[材料M]` = "材"
  - `F` present (but NOT part of `DF`) → `[器材F]` = "器"
  - `DF` present → `[法器DF]` = "法"

## Capabilities

### New Capabilities
- (none — this is a correction to existing parsing behaviour)

### Modified Capabilities
- `core`: The component parsing requirement now explicitly mandates letter-abbreviation (V/S/M/F/DF) detection in addition to Chinese-character detection.

## Impact

- `app.py` — `parse_spell_data` function, component parsing block only.
- No new dependencies, no API changes, no schema changes.
