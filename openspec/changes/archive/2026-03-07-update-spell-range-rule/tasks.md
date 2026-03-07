## 1. Update Extraction Logic

- [x] 1.1 Locate the spell range extraction logic in `app.py` (e.g., inside `extract_spell_data` or similar function).
- [x] 1.2 Implement Rule 1: Check if the range string starts with "近距", "中距", "遠距", or "接觸" and return those first 2 characters.
- [x] 1.3 Implement Rule 2: If Rule 1 fails, check if the stripped string length is <= 4, and return it exactly as is.
- [x] 1.4 Implement Rule 3: If both Rule 1 and Rule 2 fail, return "其他".

## 2. Testing and Verification

- [ ] 2.1 Verify the extraction logic against a test subset or mock strings to ensure all 3 scenarios from the specs evaluate correctly.
- [ ] 2.2 Run a dry-run or target a test row in the Google Sheet to confirm the parsed data is written back correctly.
