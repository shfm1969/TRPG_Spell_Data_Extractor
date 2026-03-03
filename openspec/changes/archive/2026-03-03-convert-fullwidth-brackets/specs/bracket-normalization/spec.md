## ADDED Requirements

### Requirement: 全形括號正規化
系統 SHALL 在將任何法術欄位值寫入 Google Sheets 之前，將文字中所有全形括號「（」「）」轉換為半形括號「(」「)」。

#### Scenario: 全形括號自動轉半形
- **WHEN** 欄位值文字含有全形左括號「（」或全形右括號「）」
- **THEN** 系統 SHALL 將「（」替換為「(」、「）」替換為「)」後再寫入試算表

#### Scenario: 不含全形括號的文字不受影響
- **WHEN** 欄位值文字不含任何全形括號
- **THEN** 系統 SHALL 保持文字內容不變，正常寫入試算表
