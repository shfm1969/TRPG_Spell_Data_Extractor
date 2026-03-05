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
- **THEN** it MUST only attempt to process rows where at least one target column (`[語言V]`, `[姿勢S]`, `[材料M]`, `[器材F]`, `[法器DF]`, `[施法時間]`, `[施法距離]`, `[持續時間]`, `[豁免說明]`, `[法抗]`) is empty and the `[法術詳述 連結]` contains a valid Google Doc URL.
- **AND** when parsing the Google Doc, the system SHALL locate the target spell block by matching the spell's English name against heading-format lines only (lines matching `中文名（English Name）` pattern). If no heading match is found, the system SHALL skip that spell and produce no updates for it.

#### Scenario: 法術名稱在文件中有標題行匹配
- **WHEN** 目標法術的英文名稱在 Google Doc 中存在對應的標題行
- **THEN** 系統 SHALL 正確定位法術區塊並解析欄位資料

#### Scenario: 法術名稱在文件中無標題行匹配
- **WHEN** 目標法術的英文名稱在 Google Doc 中不存在對應的標題行（僅出現在其他法術描述中）
- **THEN** 系統 SHALL 跳過該法術，不寫入任何資料到試算表

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
- **THEN** the `[持續時間]` text SHALL first have 「每等級」replaced with 「每CL」, then retained if its length is <= 16 characters, otherwise return 「其他」.
- **AND** the `[豁免說明]` text must be retained if its length is <= 16 characters, otherwise return 「其他」.
- **AND** the `[法術抗力]` text must be retained if its length is <= 5 characters, otherwise return 「其他」.
