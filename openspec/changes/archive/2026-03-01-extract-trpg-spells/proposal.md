# Proposal: Automate TRPG Spell Data Extraction to Google Sheets

## Context
The user needs to automate the process of extracting spell details from Google Docs and updating a specific TRPG Google Sheet ("法術詳述列表_大叔" located in "我的雲端硬碟/5團資料_大叔/卡爾_牧師_20260227"). Currently, this process is manual and time-consuming. 

## Goals
- Create a Python script using Google Drive, Docs, and Sheets APIs.
- Automatically find the target Google Sheet.
- Iterate through rows with missing spell data, starting from a user-specified row number and processing up to a user-specified limit (maximum 100 rows per execution).
- Read the linked Google Docs to extract specific spell components (V, S, M, F, DF), casting time, range, duration, saving throw, and spell resistance based on predefined rules.
- Batch update the extracted data back into the Google Sheet.
- Ensure all API credentials and environmental configurations are securely managed via `.env` and `.gitignore`, utilizing `uv` for environment management.

## Impact
- **Efficiency**: Eliminates manual data entry for TRPG spell management.
- **Accuracy**: Reduces human error by automatically parsing and mapping specific keywords based on consistent rules.
- **Codebase**: Introduces a new standalone Python project (`google-disk-operation`) secured with OAuth 2.0. No existing application architecture is modified, but new dependency configurations (`pyproject.toml`, `uv`) are established.
