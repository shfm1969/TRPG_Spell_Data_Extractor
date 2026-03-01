# Specification: TRPG Spell Data Extraction

## Feature Context
The pipeline must extract specific Dungeons & Dragons (or Pathfinder) spell properties from a text document and accurately map them to predefined single-character codes or abbreviated descriptions in a spreadsheet.

## Requirements

### Requirement: Authentication and File Discovery
- **GIVEN** a user running the script locally
- **WHEN** the script executes
- **THEN** it must either prompt for browser OAuth 2.0 or use a valid `token.json`
- **AND** it must locate the folder "我的雲端硬碟/5團資料_大叔/卡爾_牧師_20260227"
- **AND** it must locate the spreadsheet "法術詳述列表_大叔" inside that folder.

### Requirement: Execution Input Constraints
- **GIVEN** the script is executed
- **WHEN** prompting the user or parsing arguments
- **THEN** it must request a `[starting Google Sheet row number]` and `[number of records]`
- **AND** it must enforce that `[number of records]` cannot exceed 100
- **AND** if a value > 100 is provided, it should either cap it at 100 or raise a validation error.

### Requirement: Missing Data Resolution
- **GIVEN** the "法術詳述列表_大叔" spreadsheet is loaded based on the `[starting row number]` and `[number of records]`
- **WHEN** the script scans the specified range of rows
- **THEN** it must only attempt to process rows where at least one target column (`[語言V]`, `[姿勢S]`, `[材料M]`, `[器材F]`, `[法器DF]`, `[施法時間]`, `[施法距離]`, `[持續時間]`, `[豁免說明]`, `[法抗]`) is empty and the `[法術詳述 連結]` contains a valid Google Doc URL.

### Requirement: Component Parsing
- **GIVEN** a Google Doc containing spell text with a "成分" (Components) section
- **WHEN** the text is evaluated
- **THEN** the script must map the components as follows:
  - If "語言" exists -> "[語言V]" = "語"
  - If "姿勢" exists -> "[姿勢S]" = "姿"
  - If "材料" exists -> "[材料M]" = "材"
  - If "器材" exists -> "[器材F]" = "器"
  - If "法器" exists -> "[法器DF]" = "法"

### Requirement: Casting Attributes Temporal and Spatial Parsing
- **GIVEN** spell text parameters for time and range
- **WHEN** the text is evaluated
- **THEN** the `[施法時間]` must map "一个标准动作" to "標動" and "一个直觉动作" to "即時", leaving others unchanged.
- **AND** the `[施法距離]` must map to "近距", "中距", or "遠距", throwing all other variants to "其他".

### Requirement: String Length Bound Constraints
- **GIVEN** spell text parameters for duration, saving throw, and spell resistance
- **WHEN** the text is evaluated
- **THEN** the `[持續時間]` text must be retained if its length is <= 2 characters, otherwise return "其他".
- **AND** the `[豁免檢定]` text must be retained if its length is <= 12 characters, otherwise return "其他".
- **AND** the `[法術抗力]` text must be retained if its length is <= 5 characters, otherwise return "其他".
