## ADDED Requirements

### Requirement: Extract Range Field According to New Rules
The system SHALL extract the "Range" (施法距離) field from the spell description document and normalize it according to specific string matching and length rules.

#### Scenario: Rule 1 - Starts with specific keywords
- **WHEN** the "Range" text starts with "近距", "中距", "遠距", or "接觸"
- **THEN** the system MUST return exactly those 2 characters (e.g., "近距").

#### Scenario: Rule 2 - Short string fallback
- **WHEN** the "Range" text does not match Rule 1, BUT its length (after stripping leading/trailing whitespace) is 4 characters or fewer (e.g., "個人", "60呎")
- **THEN** the system MUST return the exact original string without truncation.

#### Scenario: Rule 3 - Catch-all fallback
- **WHEN** the "Range" text does not match Rule 1 and its length is greater than 4 characters
- **THEN** the system MUST return the string "其他".

## MODIFIED Requirements

*(No existing requirements are modified in this spec update, as this is a new spec for this specific change)*

## REMOVED Requirements

*(None)*
