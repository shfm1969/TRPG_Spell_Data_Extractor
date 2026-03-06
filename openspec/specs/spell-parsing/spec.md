## ADDED Requirements

### Requirement: Accurate Spell Text Boundary Detection
The system MUST correctly detect the end of a spell's text block by identifying the title of the next spell, even when the next spell's title contains numbers or punctuation characters like commas (`,`), forward slashes (`/`), and smart quotes (`’`).

#### Scenario: Spell title contains punctuation
- **WHEN** the document contains a spell whose English name includes a smart quote, comma, slash, or numbers (e.g., `Bull’s Strength, Mass`)
- **THEN** the parser MUST correctly identify this line as a subheading
- **THEN** the parser MUST NOT swallow this spell's text into the preceding spell's extracted block
- **THEN** components and properties from this spell MUST NOT be mistakenly attributed to the previous spell
