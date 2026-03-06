## MODIFIED Requirements

### Requirement: String Length Bound Constraints
- **GIVEN** spell text parameters for duration, saving throw, and spell resistance
- **WHEN** the text is evaluated
- **THEN** the `[持續時間]` text SHALL first have 「每等級」replaced with 「每CL」, then retained if its length is <= 16 characters, otherwise return 「其他」.
- **AND** the `[豁免說明]` text must be retained if its length is <= 16 characters, otherwise return 「其他」.
- **AND** the `[法抗]` field SHALL be mapped by keyword from the `法術抗力` line as follows:
  - Content starts with "不可" → `[法抗]` = "不可"
  - Content starts with "可" → `[法抗]` = "可"
  - Content starts with "否" → `[法抗]` = "否"
  - Anything else → `[法抗]` = "其他"

#### Scenario: 法抗為「不可」
- **WHEN** `法術抗力` 行內容以「不可」開頭
- **THEN** 系統 SHALL 將 `[法抗]` 設為 "不可"

#### Scenario: 法抗為「可」
- **WHEN** `法術抗力` 行內容以「可」開頭
- **THEN** 系統 SHALL 將 `[法抗]` 設為 "可"

#### Scenario: 法抗為「否」
- **WHEN** `法術抗力` 行內容以「否」開頭
- **THEN** 系統 SHALL 將 `[法抗]` 設為 "否"

#### Scenario: 法抗無法辨識
- **WHEN** `法術抗力` 行內容不以上述任何關鍵字開頭
- **THEN** 系統 SHALL 將 `[法抗]` 設為 "其他"

## ADDED Requirements

### Requirement: Verbose Diagnostic Output
- **GIVEN** the script is invoked with `--verbose`
- **WHEN** processing each row
- **THEN** the system SHALL print to stdout:
  - Per row in filter stage: whether the row was queued or skipped, and the reason for skipping
  - In `parse_spell_data`: the derived `target_name` used for heading search
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
