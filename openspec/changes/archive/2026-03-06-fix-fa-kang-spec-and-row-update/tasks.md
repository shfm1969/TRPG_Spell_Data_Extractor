## 1. Add --verbose Flag

- [x] 1.1 In `main()`, add `parser.add_argument("--verbose", action="store_true", help="Print diagnostic output for each row.")` and pass `args.verbose` through to relevant functions
- [x] 1.2 Add `verbose: bool = False` parameter to `filter_rows_for_processing`; print per-row skip reason when `verbose=True` (skipped: no URL / invalid URL / all fields filled)
- [x] 1.3 Print "Row N: queued for processing" in `filter_rows_for_processing` when row passes filter and `verbose=True`
- [x] 1.4 Add `verbose: bool = False` parameter to `parse_spell_data`; print derived `target_name` at entry when `verbose=True`
- [x] 1.5 In `parse_spell_data` heading search, print matched line + index when found and `verbose=True`; print "no heading match → skipping" when `for/else` triggers and `verbose=True`
- [x] 1.6 In `main()` processing loop, print the `parsed_data` dict returned by `parse_spell_data` when `verbose=True`

## 2. Verification

- [x] 2.1 Run `uv run app.py --start-row 549 --batch-size 1 --verbose` and inspect output to identify the failure stage
- [x] 2.2 Confirm that running without `--verbose` produces identical output to before (no extra lines)

## 3. Fix Trad/Simp Heading Mismatch

- [x] 3.1 在模組層級新增 `_t2s_converter = opencc.OpenCC('t2s')` 繁→簡轉換器
- [x] 3.2 在 `parse_spell_data` 的標題搜尋迴圈中，計算 `target_name_simp = _t2s_converter.convert(target_name).lower()`，並在 `in line_lower` 判斷時同時檢查繁體與簡體版本
- [x] 3.3 Verbose 模式下，一併印出 `target_name_simp` 以方便確認
- [x] 3.4 修正 `[法抗]` 解析邏輯以符合需求說明：「有」/「可」→"可"；「否」/「无」/「無」/「不可」→"不可"
- [x] 3.5 手動測試：`uv run app.py --start-row 549 --batch-size 2 --verbose` 確認兩列均成功解析並寫入
