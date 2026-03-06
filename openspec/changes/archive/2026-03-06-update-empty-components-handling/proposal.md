## Why

According to the updated requirements (`需求說明.md`), if a spell component is missing (Language, Somatic, Material, Focus, or Divine Focus), the script should output an empty string ("空白") instead of ignoring the field or leaving it unchanged. Currently, if a component is missing in the document, `parse_spell_data` does not set a key in `parsed_data`, which means the corresponding cell in the Google Sheet is either skipped or retains old data. We need to implement this explicit empty-string assignment to fully comply with the latest rules.

## What Changes

- Update `parse_spell_data` in `app.py` to initialize component properties (`[語言V]`, `[姿勢S]`, `[材料M]`, `[器材F]`, `[法器DF]`) with an empty string (`""`) by default.
- Ensure that if the component is indeed not found during the text parsing block, the empty string is correctly returned for these specific fields.

## Capabilities

### New Capabilities
*(None)*

### Modified Capabilities
- `spell-parsing`: Updated the handling algorithm for spell components (V, S, M, F, DF) to explicitly yield an empty string when absent, modifying how omitted properties are mapped to the extracted output.

## Impact

- **Affected Code**: `app.py` (`parse_spell_data` function).
- **Behavior**: Five specific component columns in the target Google Sheet will be explicitly overwritten with empty strings if the spell lacks those components in the source Google Doc.
