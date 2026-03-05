# Proposal: Update Default Target Folder Path

## Why
The current default target folder path is hardcoded to a specific character's folder (`5團資料_大叔/卡爾_牧師_20260227`). This restricts the application's utility when processing sheets for other characters or general data within the campaign folder. Updating the path to `5團資料_大叔` will make the default configuration more general and applicable to the whole campaign.

## What Changes
- Update the default `TARGET_FOLDER_NAME` environment variable fallback in `app.py`.
- Update references in `README.md`.
- No new features are added; this is a configuration/default value change.

## Impact
- **Affected code**: `app.py`
- **Documentation**: `README.md`
- **Users**: Users will naturally search in the parent campaign directory instead of a specific character's directory, which might match broader or different sheets.
