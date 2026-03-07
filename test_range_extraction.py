import io
import sys
from app import parse_spell_data

# Ensure stdout uses UTF-8 so printing Chinese characters won't crash
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

tests = [
	"施法距離: 近距 (25呎 + 5呎/每2個等級)",
	"施法距離：中距 (100呎 + 10呎/每等級)",
	"施法距離：遠距 (400呎 + 40呎/每等級)",
	"施法距離: 接觸",
    "施法距离：接触",
	"施法距離：個人",
	"施法距離：60 呎",
    "施法距離：10 呎",
	"施法距離：很遠很遠",
    "施法距離:長度超過五字"
]

print("Testing Spell Range Extraction Rules:")
print("-" * 50)
for t in tests:
	# Add a dummy spell name to make the parser work
    text_block = f"TestSpell (TestSpell)\n{t}"
    res = parse_spell_data(text_block, "TestSpell")
    extracted_range = res.get("[施法距離]", "")
    print(f"Input: {t}")
    print(f"Output: '{extracted_range}'")
    print("-" * 50)
