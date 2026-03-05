## MODIFIED Requirements

### Requirement: Authentication and File Discovery
- **GIVEN** a user running the script locally
- **WHEN** the script executes
- **THEN** it must either prompt for browser OAuth 2.0 or use a valid `token.json`
- **AND** it must locate the folder "我的雲端硬碟/5團資料_大叔"
- **AND** it must locate the spreadsheet "法術詳述列表_大叔" inside that folder.

#### Scenario: 成功連線並找到目標資料夾與檔案
- **WHEN** 使用者執行腳本且授權成功
- **THEN** 系統必須成功找到預設的 "我的雲端硬碟/5團資料_大叔" 資料夾與 "法術詳述列表_大叔" 試算表
