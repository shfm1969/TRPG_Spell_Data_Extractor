## MODIFIED Requirements

### Requirement: Component Parsing
- **GIVEN** a Google Doc containing spell text with a "成分" (Components) section
- **WHEN** the text is evaluated
- **THEN** the script MUST map the components as follows (Chinese-character OR letter token — either is sufficient):
  - If "語言" OR "语言" OR "言语" OR "言語" OR the token `V` is present → `[語言V]` = "語"
  - If "姿勢" OR "姿势" OR the token `S` is present → `[姿勢S]` = "姿"
  - If "材料" OR the token `M` is present → `[材料M]` = "材"
  - If "器材" OR a standalone `F` (not preceded by `D`) is present → `[器材F]` = "器"
  - If "法器" OR the token `DF` is present → `[法器DF]` = "法"
- **AND** "standalone F" SHALL be determined by regex `(?<![A-Z])F(?![A-Z])` applied to the component line.
- **AND** the `DF` token check SHALL be performed before the standalone `F` check to prevent false positives.

#### Scenario: 成分以字母縮寫列出
- **WHEN** 成分行內容為 "成分：V, S, M"
- **THEN** 系統 SHALL 將 `[語言V]` = "語"、`[姿勢S]` = "姿"、`[材料M]` = "材"

#### Scenario: 成分同時包含 DF 與 S
- **WHEN** 成分行內容為 "成分：DF, S"
- **THEN** 系統 SHALL 將 `[法器DF]` = "法"、`[姿勢S]` = "姿"，且 `[器材F]` 不得被設值

#### Scenario: 成分以中文字列出（既有行為不變）
- **WHEN** 成分行內容為 "成分：語言、姿勢、材料"
- **THEN** 系統 SHALL 將 `[語言V]` = "語"、`[姿勢S]` = "姿"、`[材料M]` = "材"

#### Scenario: 成分以混合方式列出
- **WHEN** 成分行內容為 "成分：語言 (V), M"
- **THEN** 系統 SHALL 正確設值 `[語言V]` = "語" 與 `[材料M]` = "材"
