# Technical Design: Automate TRPG Spell Data Extraction

## Context
The goal is to automate the extraction of TRPG spell details from Google Docs into a specific Google Sheet ("法術詳述列表_大叔"). This requires a Python script that integrates Google Drive API (for file discovery), Google Sheets API (for reading and writing data), and Google Docs API (for parsing text content).

## Goals / Non-Goals
**Goals:**
- Secure OAuth 2.0 authentication strictly using local `credentials.json` and `token.json`.
- Accurately locate the target Google Sheet via recursive logical paths in Google Drive.
- Read the active sheet and filter rows where spell data (V, S, M, F, DF, etc.) is missing.
- Fetch Google Doc text via the URL provided in the "[法術詳述 連結]" column.
- Parse the document text based on strict mapping rules.
- Batch update the parsed values back into the Google Sheet.

**Non-Goals:**
- Developing a web interface or frontend application.
- Overwriting existing, manually entered spell data in the Google Sheet.
- Supporting general data extraction outside the specified TRPG spell format rules.

## Design Details

### 1. Authentication & Configuration
- **Libraries**: `google-auth-oauthlib`, `google-auth-httplib2`, `google-api-python-client`.
- **Flow**: Use `InstalledAppFlow` to trigger browser authentication on the first run. Save the resulting credentials to `token.json` for subsequent headless executions.
- **Environment Management**: Use `python-dotenv` to load configurations (e.g., Target Folder Name, Target Sheet Name).

### 2. File Discovery (Drive API)
- Use `files().list()` method with `q` parameter to find the folder "我的雲端硬碟/5團資料_大叔/卡爾_牧師_20260227" and retrieve its ID.
- Query again within that Folder ID to find the file ID of the Spreadsheet "法術詳述列表_大叔".

### 3. Execution Control & Data Retrieval (Sheets API & Docs API)
- **Execution Input**: The script requires two inputs at runtime:
  1. `start_row`: The row number in the Google Sheet to begin scanning.
  2. `batch_size`: The number of rows to process in this execution (must be clamped to a maximum of 100 to prevent API exhaustion).
- **Sheets API**: Call `spreadsheets().values().get()` to fetch rows starting from `start_row` up to `start_row + batch_size`. Filter the dataset to identify rows where specific target columns (e.g., `[語言V]` to `[法抗]`) are empty.
- **Docs API**: Extract the Document ID from the URL in the `[法術詳述 連結]` column. Call `documents().get()` to fetch the structural elements of the Doc. Extract and concatenate the text elements into a single string for parsing.

### 4. Parsing Logic (Business Rules)
Apply regex or string matching on the extracted Doc text:
- **Components (`[語言V]`, `[姿勢S]`, `[材料M]`, `[器材F]`, `[法器DF]`)**: Search for the presence of specific keywords (語言, 姿勢, 材料, 器材, 法器) within the "成分" section. Map to (語, 姿, 材, 器, 法) respectively.
- **Casting Time (`[施法時間]`)**: Map "一个标准动作" to "標動", "一个直觉动作" to "即時", else return original text.
- **Range (`[施法距離]`)**: Extract "近距", "中距", or "遠距", else return "其他".
- **Duration (`[持續時間]`)**: Return original text if length <= 2 characters, else "其他".
- **Saving Throw (`[豁免說明]`)**: Return original text from the `[豁免检定]` section if length <= 12 characters, else "其他".
- **Spell Resistance (`[法抗]`)**: Return original text from the `[法术抗力]` section if length <= 5 characters, else "其他".

### 5. Data Write-Back (Sheets API)
- Format the parsed results into a list of `ValueRange` objects corresponding to their specific cell coordinates.
- Call `spreadsheets().values().batchUpdate()` to write all changes back to the Google Sheet in a single API call to optimize performance.

## Risks / Trade-offs
- **API Rate Limits**: Google APIs have quota limits. Using `batchUpdate` minimizes Sheets API calls, but Docs API will require one call per URL. Added short delays (rate limiting) if the number of missing rows is exceptionally large.
- **Document Formatting Variability**: If the format of the source Google Docs varies significantly from expected structures, the parsing logic might fail to extract data correctly. To mitigate this, unparseable fields will be safely ignored or flagged rather than crashing the script.
