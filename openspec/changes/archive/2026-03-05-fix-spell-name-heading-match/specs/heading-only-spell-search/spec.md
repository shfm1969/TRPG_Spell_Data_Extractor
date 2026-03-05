## ADDED Requirements

### Requirement: Heading-Only Spell Name Search
`parse_spell_data` 搜尋目標法術名稱時，SHALL 僅匹配標題行格式（中文名稱後接括號包裹的英文名稱），不得匹配描述文字中的引用。

#### Scenario: 法術名稱同時出現在標題行與其他法術描述中
- **WHEN** 文件中 `antimagic field` 同時出現在 Air Walk 的描述文字與 `反魔場（Antimagic Field）` 標題行
- **THEN** 系統 SHALL 選擇標題行 `反魔場（Antimagic Field）` 作為法術區塊起點

#### Scenario: 文件中僅在描述文字中提及法術名稱而無標題行
- **WHEN** 文件中不存在包含目標法術名稱的標題行
- **THEN** 系統 SHALL 放棄該法術的解析，回傳空結果（不寫入任何資料）
