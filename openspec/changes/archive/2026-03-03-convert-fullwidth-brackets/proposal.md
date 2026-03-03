## Why

從 Google Doc 擷取的法術文字中，括號有時以全形「（）」呈現（常見於中文排版），但試算表欄位預期使用半形「()」進行後續比對與顯示。統一轉換能確保資料格式一致，避免因括號形式不同造成的比對失敗或顯示異常。

## What Changes

- **括號正規化**：在將欄位值寫入 Google Sheets 之前，將文字中所有全形括號「（」「）」轉換為半形「(」「)」。

## Capabilities

### New Capabilities
- `bracket-normalization`: 對所有擷取的法術欄位文字執行全形→半形括號轉換

### Modified Capabilities

（無）

## Impact

- `app.py`：在既有的 `to_zh_tw()` 呼叫之後，新增括號轉換步驟；或擴充 `to_zh_tw()` helper 使其一併處理括號替換。
- 無 API 介面或結構性破壞性變更。
