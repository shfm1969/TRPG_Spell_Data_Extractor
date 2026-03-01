# Implementation Tasks: TRPG Spell Data Extraction

## 1. Setup and Authentication
- [x] 1.1 Initialize the Python project structure and install dependencies (`uv add google-api-python-client google-auth-httplib2 google-auth-oauthlib python-dotenv`).
- [x] 1.2 Implement OAuth 2.0 flow using `InstalledAppFlow` to generate and save `token.json`.
- [x] 1.3 Create `.env` template and set up configuration loading using `python-dotenv`.

## 2. File Discovery (Drive API)
- [x] 2.1 Implement `find_folder_id(name, parent_id)` to locate "我的雲端硬碟/5團資料_大叔/卡爾_牧師_20260227".
- [x] 2.2 Implement `find_file_id(name, parent_id)` to locate the "法術詳述列表_大叔" Google Sheet.

## 3. Execution Control and Spreadsheet Data Retrieval (Sheets API)
- [x] 3.1 Implement runtime input for `start_row` and `batch_size`, including validation to ensure `batch_size <= 100`.
- [x] 3.2 Fetch rows from the target Google Sheet using range `start_row` to `start_row + batch_size`.
- [x] 3.3 Filter rows to identify those missing data in target columns but containing a valid Google Doc URL in the `[法術詳述 連結]` column.

## 4. Document Parsing (Docs API)
- [x] 4.1 Extract Google Doc ID from the provided URL.
- [x] 4.2 Fetch document content using Docs API and concatenate text elements.
- [x] 4.3 Implement extraction logic for Spell Components (V, S, M, F, DF).
- [x] 4.4 Implement extraction logic for Casting Time and Range.
- [x] 4.5 Implement extraction logic and length constraints for Duration, Saving Throw, and Spell Resistance.

## 5. Data Write-Back (Sheets API)
- [x] 5.1 Format the extracted text into `ValueRange` objects corresponding to their specific sheet cells.
- [x] 5.2 Execute a `batchUpdate` request to write all parsed data back into the Google Sheet efficiently.

## 6. Testing and Refinement
- [x] 6.1 Test the authentication flow and `.env` loading.
- [x] 6.2 Run a dry-run test (printing parsed values without writing to Sheets) on a small subset of links.
- [x] 6.3 Execute a full end-to-end test and verify the Google Sheet is updated correctly according to the rules.
