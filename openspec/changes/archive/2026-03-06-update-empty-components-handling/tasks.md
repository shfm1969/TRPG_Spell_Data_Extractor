## 1. Feature Implementation

- [x] 1.1 In `app.py`, update `parse_spell_data` to initialize `parsed_data` with empty strings (`""`) for `[語言V]`, `[姿勢S]`, `[材料M]`, `[器材F]`, and `[法器DF]`.

## 2. Verification

- [x] 2.1 Test locally using `test.py` against a spell that has partial components (e.g. only V and S) to ensure M, F, and DF output empty strings.
- [x] 2.2 Verify that other properties (like duration, casting time) remain unaffected by this dictionary seeding.
