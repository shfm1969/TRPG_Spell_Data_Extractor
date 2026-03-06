## Context

The `app.py` script automatically parses text blocks of spells to extract various properties into a data dictionary (`parsed_data`), which is then mapped to the structure of the target Google Sheet. Currently, if a specific component (e.g., Material Component) is not found in the spell's description block, the script simply omits adding a key for it in the `parsed_data` dictionary. As a result, when writing back to the spreadsheet, these empty components might retain their old values in the spreadsheet, or behave inconsistently depending on downstream update logic. New requirements state that omitted spell components must definitively be replaced with an empty string ("空白") to clear out any old spreadsheet data.

## Goals / Non-Goals

**Goals:**
- Guarantee that if `[語言V]`, `[姿勢S]`, `[材料M]`, `[器材F]`, or `[法器DF]` is truly missing from a spell, the payload sent to update the Google Sheet explicitly contains an empty string (`""`) for those fields.

**Non-Goals:**
- Altering the extraction conditions or regexes used to find the existing components.
- Modifying how other fields (like Duration, Saving Throw, Casting Range) are handled, unless specifically requested.

## Decisions

- **Initial Dictionary Seeding:** We will pre-populate the `parsed_data` dictionary inside `parse_spell_data` with empty strings for all five component properties.
  - *Rationale*: If the subsequent lines of the text parser find the components, they will overwrite these empty strings with the correct extracted values. If they do not find the components, the keys will retain the empty strings, securely persisting the "空白" logic back to the sheet update phase. This approach ensures safety and zero regressions on existing extraction logic.

## Risks / Trade-offs

- **Risk:** Existing row data in the spreadsheet for these five columns might be overwritten with blanks if extraction fails unexpectedly due to formatting anomalies.
  - *Mitigation:* The requirement explicitly states to overwrite with blanks if not found, aligning perfectly with business rules. The existing tests should verify this functionality against spells that deliberately omit certain components.
