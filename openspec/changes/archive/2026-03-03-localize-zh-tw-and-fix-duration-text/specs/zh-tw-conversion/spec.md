## ADDED Requirements

### Requirement: 繁體中文轉換
系統 SHALL 在將任何法術欄位值寫入 Google Sheets 之前，先將文字從簡體中文轉換為繁體中文（臺灣用字）。

#### Scenario: 簡體文字自動轉繁體
- **WHEN** 系統從 Google Doc 擷取到簡體中文的法術文字
- **THEN** 系統 SHALL 使用 `opencc-python-reimplemented`（設定 `s2twp.json`）將文字轉為繁體中文
- **AND** 轉換後的繁體文字才被寫入對應的 Google Sheets 欄位

#### Scenario: 已是繁體或純數字文字不變
- **WHEN** 擷取的文字本身已是繁體中文或純數字符號
- **THEN** 轉換後文字內容 SHALL 保持不變（opencc 不會破壞正確繁體）
