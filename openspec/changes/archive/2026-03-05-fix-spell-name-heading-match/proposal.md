## Why

`parse_spell_data` 在搜尋目標法術名稱時，使用「第一個包含該名稱的行」作為法術區塊起點。當法術名稱出現在其他法術的描述文字中（例如 `antimagic field` 出現在 Air Walk 的描述裡），會錯誤地將該描述行作為起點，導致解析區塊不含任何欄位資料（成分、施法時間等），最終回傳空結果、無法更新試算表。

## What Changes

- 修改 `parse_spell_data` 中的法術名稱搜尋邏輯：**僅匹配標題行格式**（如 `反魔場（Antimagic Field）`），不再匹配描述文字中的引用
- 若在文件中找不到標題行格式的匹配，直接放棄該法術的解析，回傳空結果

## Capabilities

### New Capabilities
- `heading-only-spell-search`: 法術名稱搜尋僅限標題行匹配，避免描述文字中的引用造成誤判

### Modified Capabilities
- `core`: 修改法術區塊定位邏輯，影響所有法術的解析行為

## Impact

- **檔案**: `app.py` — `parse_spell_data` 函式
- **行為變更**: 找不到標題行匹配時，該法術不會被解析（之前會匹配到錯誤的位置並產生空結果）
