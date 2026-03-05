## 1. 修改法術名稱搜尋邏輯

- [x] 1.1 在 `parse_spell_data` 中新增標題行格式 regex `heading_like`，僅匹配 `中文名（English Name）` 格式的行
- [x] 1.2 使用 `for...else` 語法：迴圈未找到標題行匹配時，直接 `return parsed_data`（空 dict）
- [x] 1.3 移除原本「匹配任意包含法術名稱的行」的邏輯

## 2. 驗證

- [x] 2.1 執行 `uv run python app.py --start-row 20` 驗證 Row 20（反魔場/Antimagic Field）可正確解析並更新 10 個儲存格
- [x] 2.2 確認不會因為 Air Walk 描述中的 `antimagic field` 引用而產生誤判
