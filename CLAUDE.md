# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Install dependencies:**
```bash
uv sync
```

**Run the extractor:**
```bash
uv run app.py --start-row <row_number> [--batch-size <count>]
```

Examples:
```bash
uv run app.py --start-row 4                    # single row
uv run app.py --start-row 10 --batch-size 50   # batch of 50 rows
```

- `--start-row`: (required) Starting row number in the Google Sheet (row 1 = header).
- `--batch-size`: (optional) Max rows to process; default 1, hard cap at 100.

## Setup Requirements

- `credentials.json` must be placed in the project root (Google OAuth 2.0 Desktop App client ID).
- On first run, a browser window opens for Google account authorization; this creates `token.json` for subsequent runs.
- Copy `.env.example` to `.env` and adjust values if needed.

**Environment variables (`.env`):**
| Variable | Default |
|---|---|
| `GOOGLE_DRIVE_ROOT_FOLDER` | `我的雲端硬碟` |
| `TARGET_FOLDER_NAME` | `5團資料_大叔` (supports sub-paths with `/`) |
| `TARGET_SHEET_NAME` | `法術詳述列表_大叔` |

## Architecture

The entire application lives in a single file: `app.py`. The execution pipeline is linear:

1. **Authentication** (`get_credentials`) — OAuth 2.0 via `token.json` / `credentials.json`.
2. **File Discovery** (`get_target_sheet_id`) — Traverses Google Drive folder path from `.env` to find the target spreadsheet ID.
3. **Sheet Fetch** (`fetch_sheet_data`) — Retrieves headers (row 1) to build a `col_map` (column name → index), then fetches the requested row range using the `spreadsheets.get` API (not `values.get`) to capture hyperlinks.
4. **Row Filtering** (`filter_rows_for_processing`) — Keeps only rows where `[法術詳述 連結]` is a valid Google Docs URL **and** at least one `TARGET_COLUMNS` cell is empty.
5. **Document Parsing** (`parse_spell_data`) — For each qualifying row, fetches the full text of the linked Google Doc (`get_doc_text`), then locates the correct spell block by matching the English name against heading-format lines only (pattern: `中文名（English Name）`). Parses spell properties line by line within that isolated block.
6. **Normalization** (`to_zh_tw`) — Converts Simplified Chinese → Traditional Chinese (Taiwan variant) via `opencc` (`s2twp` profile) and replaces fullwidth brackets `（）` with halfwidth `()`.
7. **Write-back** — Collects all cell updates and submits them in a single `batchUpdate` call.

### Key Design Decisions

- **Heading-only spell matching**: `parse_spell_data` only starts extraction from a line that matches `^[^:：]{0,20}[(（].*[)）]\s*$` (a short title with parenthesized name). If no such heading is found, the spell is skipped entirely — this prevents false matches from casual mentions of a spell name inside another spell's description.
- **Spell block isolation**: After finding the start heading, the parser scans forward until the next heading-format line to define the block boundary, ensuring multi-spell documents don't bleed data across entries.
- **Column lookup** (`get_col_idx`): Tries column names both with and without surrounding `[]` brackets to handle header variations.
- **No overwrites of existing data**: Only rows with at least one empty target column are processed.

## OpenSpec Workflow

This project uses an OpenSpec-based change management workflow. Specs live in `openspec/specs/` and change history is archived in `openspec/changes/archive/`. Use the `/opsx:propose`, `/opsx:apply`, and `/opsx:archive` slash commands (or the equivalent skills) to manage changes.
