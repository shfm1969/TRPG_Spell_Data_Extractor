## Context

The current `TARGET_FOLDER_NAME` in `app.py` defaults to "5團資料_大叔/卡爾_牧師_20260227". This path was likely used during initial development or for a specific use case, but it's too narrow for general use by other players or for broader folder searches within the campaign.

## Goals / Non-Goals

**Goals:**
- Broaden the default target folder path so the script can be used more generally across the "5團資料_大叔" campaign folder without requiring users to override the environment variable unless they have a specific subfolder.

**Non-Goals:**
- Renaming the actual Google Drive folders.
- Changing the core logic of how folders or files are searched.
- Adding complex configuration management; the environment variable approach remains.

## Decisions

- **Decision**: Update `TARGET_FOLDER_NAME` default value in `os.getenv` to "5團資料_大叔" instead of "5團資料_大叔/卡爾_牧師_20260227".
  - *Rationale*: A higher-level folder allows the Google Drive API search (which typically searches recursively or within a specified parent) to find the target spreadsheet even if it's placed in a different subfolder under the campaign directory.
  - *Alternative*: Keep it as-is and force users to set `TARGET_FOLDER_NAME`. This is less user-friendly out of the box.

## Risks / Trade-offs

- **Risk**: Searches might take slightly longer or return multiple matches if there are identically named files across different character subfolders within the campaign folder.
  - *Mitigation*: The current script logic already handles file matching. If there are duplicate target sheet names, users might need to specify the exact subfolder. The README will be updated to clarify this behavior.
