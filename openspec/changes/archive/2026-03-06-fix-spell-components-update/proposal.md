## Why

When parsing spell data from Google Docs, the system needs to correctly identify the end of one spell's text block by looking for the heading of the next spell. Previously, the regular expression used to detect spell headings did not account for punctuation such as smart quotes (`’`) or commas (`,`) in spell names (e.g., `Bull’s Strength, Mass`). This caused the parser to fail to recognize the boundary, swallow subsequent spells' text into the current spell's block, and incorrectly extract properties like `[材料M]` or `[法器DF]` that belonged to those later spells. We need this fix to ensure data integrity during extraction.

## What Changes

- Update `heading_pattern` regular expression in `app.py`'s `parse_spell_data` function.
- Broaden the allowed characters within the spell name parenthesis to include numbers (`0-9`), smart quotes (`’`), commas (`,`), and forward slashes (`/`).

## Capabilities

### New Capabilities
*(None)*

### Modified Capabilities
- `spell-parsing`: Improved text block boundary detection to prevent cross-spell property pollution.

## Impact

- **Affected Code**: `app.py` (`parse_spell_data` function).
- **Behavior**: More accurate isolation of individual spell text blocks, preventing false positive attribute extraction.
