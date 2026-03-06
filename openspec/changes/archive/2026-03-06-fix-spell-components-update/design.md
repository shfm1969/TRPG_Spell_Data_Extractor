## Context
The script `app.py` extracts spell properties from a single, contiguous text block belonging to a specific spell. To isolate this text block from a larger Google Doc, the system identifies the start of the spell by finding its title, and identifies the end of the spell by finding the title of the *next* spell in the document. 
Previously, the regular expression `heading_pattern` used to detect spell titles was too restrictive (`^[^:：\(（]+[(（][a-zA-Z\s\-\']+[)）]\s*$`). It failed to match legitimate spell names containing commas (`,`) or intelligent quotes (`’`), such as "牛之力量（Bull’s Strength）" or "群体牛之力量（Bull’s Strength, Mass)". When the regex failed, the script would incorrectly continue reading into the next spell's text, thereby falsely extracting components (like `[材料M]`) that belonged to subsequent spells.

## Goals / Non-Goals

**Goals:**
- Correctly identify the end of a block of spell text even when subsequent spell titles contain punctuation like smart quotes, commas, numbers, or slashes.
- Prevent extraction of incorrect components or fields that belong to a different spell.

**Non-Goals:**
- Completely rewriting the document parsing system or moving away from regex-based extraction.

## Decisions

- **Regex Expansion**: We will update the `heading_pattern` inside `parse_spell_data` (in `app.py`) to `^[^:：\(（]+[(（][a-zA-Z0-9\s\-\'’,\/]+[)）]\s*$`.
  - *Rationale*: This explicitly supports the characters `0-9`, `’`, `,`, and `/` within the English name portion (inside the parentheses) of the spell heading. This change is minimal, isolated to the regex, and fixes the boundary detection bug without altering the broader logic.
  - *Alternatives Considered*: We considered fully parsing the Google Doc structure via styling (e.g., detecting "Heading 1" format). However, this would require significantly more API calls and logic changes, and the text structure isn't always perfectly formatted with Google Docs Heading styles anyway.

## Risks / Trade-offs

- **Risk: False Positives**: The broader regex could potentially match lines of normal text that happen to resemble `(Chinese Name)（English Name)` with these characters.
  - *Mitigation*: The regex strictly requires no leading colons up to the opening parenthesis, forces a specific structure, and checks that this is the ENTIRE line (with `^` and `$`). This structure is highly unique to the headings in the source document.
