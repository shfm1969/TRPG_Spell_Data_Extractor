## MODIFIED Requirements

### Requirement: Extract Component Requirements
The parser MUST correctly identify and extract Language, Somatic, Material, Focus, and Divine Focus components.
- Components are found on lines beginning with "成分", "法术成分", or "法術成分".
- If the line contains "語言", "语言", "言语", "言語", or isolated "V", the `[語言V]` field MUST be set to "語". Otherwise, it MUST be set to an empty string ("").
- If the line contains "姿勢", "姿势", or isolated "S", the `[姿勢S]` field MUST be set to "姿". Otherwise, it MUST be set to an empty string ("").
- If the line contains "材料" or isolated "M", the `[材料M]` field MUST be set to "材". Otherwise, it MUST be set to an empty string ("").
- If the line contains "器材" or an isolated "F" (not part of "DF"), the `[器材F]` field MUST be set to "器". Otherwise, it MUST be set to an empty string ("").
- If the line contains "法器" or isolated "DF", the `[法器DF]` field MUST be set to "法". Otherwise, it MUST be set to an empty string ("").

#### Scenario: Spell has V and S components but no M, F, or DF
- **WHEN** the spell's components line is: `法術成分：言語，姿勢`
- **THEN** `[語言V]` MUST be "語"
- **THEN** `[姿勢S]` MUST be "姿"
- **THEN** `[材料M]` MUST be an empty string ("")
- **THEN** `[器材F]` MUST be an empty string ("")
- **THEN** `[法器DF]` MUST be an empty string ("")

#### Scenario: Spell has no component line or is completely missing components
- **WHEN** the spell's descriptions omit the component line entirety
- **THEN** all five component fields (`[語言V]`, `[姿勢S]`, `[材料M]`, `[器材F]`, `[法器DF]`) MUST be explicitly set to an empty string ("")


## ADDED Requirements

### Requirement: Extract Range Field According to New Rules
The system SHALL extract the "Range" (施法距離) field from the spell description document and normalize it according to specific string matching and length rules.

#### Scenario: Rule 1 - Starts with specific keywords
- **WHEN** the "Range" text starts with "近距", "中距", "遠距", or "接觸"
- **THEN** the system MUST return exactly those 2 characters (e.g., "近距").

#### Scenario: Rule 2 - Short string fallback
- **WHEN** the "Range" text does not match Rule 1, BUT its length (after stripping leading/trailing whitespace) is 4 characters or fewer (e.g., "個人", "60呎")
- **THEN** the system MUST return the exact original string without truncation.

#### Scenario: Rule 3 - Catch-all fallback
- **WHEN** the "Range" text does not match Rule 1 and its length is greater than 4 characters
- **THEN** the system MUST return the string "其他".
