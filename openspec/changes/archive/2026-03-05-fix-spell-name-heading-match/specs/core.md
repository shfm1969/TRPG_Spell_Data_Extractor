## MODIFIED Requirements

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
