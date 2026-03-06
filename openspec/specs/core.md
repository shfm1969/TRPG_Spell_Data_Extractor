# Specification: TRPG Spell Data Extraction

## Feature Context
The pipeline must extract specific Dungeons & Dragons (or Pathfinder) spell properties from a text document and accurately map them to predefined single-character codes or abbreviated descriptions in a spreadsheet.

## Requirements

### Requirement: Authentication and File Discovery
- **GIVEN** a user running the script locally
- **WHEN** the script executes
- **THEN** it must either prompt for browser OAuth 2.0 or use a valid `token.json`
- **AND** it must locate the folder "我的雲端硬碟/5團資料_大叔"
- **AND** it must locate the spreadsheet "法術詳述列表_大叔" inside that folder.

#### Scenario: 成功連線並找到目標資料夾與檔案
- **WHEN** 使用者執行腳本且授權成功
- **THEN** 系統必須成功找到預設的 "我的雲端硬碟/5團資料_大叔" 資料夾與 "法術詳述列表_大叔" 試算表

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
- **AND** the heading search SHALL compare against both the Traditional Chinese form and the Simplified Chinese form of the target name (converted via `t2s`) to handle documents whose headings use Simplified Chinese while the spreadsheet stores Traditional Chinese.

#### Scenario: 法術名稱在文件中有標題行匹配
- **WHEN** 目標法術的英文名稱在 Google Doc 中存在對應的標題行
- **THEN** 系統 SHALL 正確定位法術區塊並解析欄位資料

#### Scenario: 法術名稱在文件中無標題行匹配
- **WHEN** 目標法術的英文名稱在 Google Doc 中不存在對應的標題行（僅出現在其他法術描述中）
- **THEN** 系統 SHALL 跳過該法術，不寫入任何資料到試算表

### Requirement: Component Parsing
- **GIVEN** a Google Doc containing spell text with a "成分" (Components) section
- **WHEN** the text is evaluated
- **THEN** the script MUST map the components as follows (Chinese-character OR letter token — either is sufficient):
  - If "語言" OR "语言" OR "言语" OR "言語" OR the token `V` is present → `[語言V]` = "語"
  - If "姿勢" OR "姿势" OR the token `S` is present → `[姿勢S]` = "姿"
  - If "材料" OR the token `M` is present → `[材料M]` = "材"
  - If "器材" OR a standalone `F` (not preceded by `D`) is present → `[器材F]` = "器"
  - If "法器" OR the token `DF` is present → `[法器DF]` = "法"
- **AND** "standalone F" SHALL be determined by regex `(?<![A-Z])F(?![A-Z])` applied to the component line.
- **AND** the `DF` token check SHALL be performed before the standalone `F` check to prevent false positives.

#### Scenario: 成分以字母縮寫列出
- **WHEN** 成分行內容為 "成分：V, S, M"
- **THEN** 系統 SHALL 將 `[語言V]` = "語"、`[姿勢S]` = "姿"、`[材料M]` = "材"

#### Scenario: 成分同時包含 DF 與 S
- **WHEN** 成分行內容為 "成分：DF, S"
- **THEN** 系統 SHALL 將 `[法器DF]` = "法"、`[姿勢S]` = "姿"，且 `[器材F]` 不得被設值

#### Scenario: 成分以中文字列出（既有行為不變）
- **WHEN** 成分行內容為 "成分：語言、姿勢、材料"
- **THEN** 系統 SHALL 將 `[語言V]` = "語"、`[姿勢S]` = "姿"、`[材料M]` = "材"

#### Scenario: 成分以混合方式列出
- **WHEN** 成分行內容為 "成分：語言 (V), M"
- **THEN** 系統 SHALL 正確設值 `[語言V]` = "語" 與 `[材料M]` = "材"

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
- **AND** the `[法抗]` field SHALL be mapped by keyword from the `法術抗力` line as follows:
  - Content starts with "不可" → `[法抗]` = "不可"
  - Content starts with "否" OR "无" OR "無" → `[法抗]` = "不可"
  - Content starts with "可" OR "有" → `[法抗]` = "可"
  - Anything else → `[法抗]` = "其他"

#### Scenario: 法抗為「不可」或「否」
- **WHEN** `法術抗力` 行內容以「不可」、「否」、「无」或「無」開頭
- **THEN** 系統 SHALL 將 `[法抗]` 設為 "不可"

#### Scenario: 法抗為「可」或「有」
- **WHEN** `法術抗力` 行內容以「可」或「有」開頭
- **THEN** 系統 SHALL 將 `[法抗]` 設為 "可"

#### Scenario: 法抗無法辨識
- **WHEN** `法術抗力` 行內容不以上述任何關鍵字開頭
- **THEN** 系統 SHALL 將 `[法抗]` 設為 "其他"

### Requirement: Verbose Diagnostic Output
- **GIVEN** the script is invoked with `--verbose`
- **WHEN** processing each row
- **THEN** the system SHALL print to stdout:
  - Per row in filter stage: whether the row was queued or skipped, and the reason for skipping
  - In `parse_spell_data`: the derived `target_name` and `target_name_simp` used for heading search
  - Heading match result: the matched line and index, or a "no heading match" message
  - Extracted fields dict returned by `parse_spell_data`
- **AND** when `--verbose` is NOT passed, output SHALL remain identical to current behavior (no extra lines).

#### Scenario: Row 被過濾掉並顯示原因
- **WHEN** 某列因缺少有效 URL 被跳過，且 `--verbose` 已啟用
- **THEN** 系統 SHALL 印出該列號與跳過原因

#### Scenario: 標題行比對失敗並顯示提示
- **WHEN** `parse_spell_data` 找不到符合的標題行，且 `--verbose` 已啟用
- **THEN** 系統 SHALL 印出 `target_name` 與 "no heading match → skipping" 訊息

#### Scenario: 成功解析並顯示欄位
- **WHEN** `parse_spell_data` 成功解析法術欄位，且 `--verbose` 已啟用
- **THEN** 系統 SHALL 印出解析出的欄位字典
