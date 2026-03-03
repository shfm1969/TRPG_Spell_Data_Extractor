## Why

目前系統從 Google Doc 取得法術原文後，直接寫入 Google Sheets，但來源文字多為簡體中文，造成試算表顯示不一致。此外，`[持續時間]` 欄位的解析對「每等級」字串的判斷需改為「每CL」，以符合遊戲術語標準。

## What Changes

- **資料本地化**：在將任何欄位值寫入 Google Sheets 之前，先對原文執行「簡體→繁體中文」轉換。
- **持續時間文字修正**：將 `[持續時間]` 解析邏輯中，識別「每等級」的字串改為識別「每CL」。

## Capabilities

### New Capabilities
- `zh-tw-conversion`: 對從 Google Doc 擷取的法術文字執行簡繁轉換，確保所有寫入值均為繁體中文。

### Modified Capabilities
- `core`: `[持續時間]` 的字串判斷規則由「每等級」改為「每CL」。

## Impact

- `app.py`：需引入或實作簡繁轉換函式，並在資料寫入前調用；同時修改 `[持續時間]` 的判斷字串。
- 無 API 介面或結構性破壞性變更。
