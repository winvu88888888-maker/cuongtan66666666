# -*- coding: utf-8 -*-
"""
TEST: Multi-intent extraction for "mấy anh chị em, nghề gì, bao nhiêu tuổi"
Verifies the green box shows ALL 3 answers.
"""
import sys, os, re
sys.path.insert(0, '.')

from free_ai_helper import FreeAIHelper

helper = FreeAIHelper()

# Question with 3 intents: count + occupation + age
question = "nhà tôi có mấy anh chị em , các anh chị em tôi đang làm nghề gì , bao nhiêu tuổi"

print("=" * 80)
print(f"QUESTION: {question}")
print("=" * 80)

# Call answer_question
result = helper.answer_question(question, chart_data=None, topic=None)

if not result:
    print("FAIL: No result!")
    sys.exit(1)

# Save full output
with open("test_multi_intent_output.txt", "w", encoding="utf-8") as f:
    f.write(result)

print(f"\nFull output length: {len(result)} chars")
print(f"Saved to test_multi_intent_output.txt")

# Check for key markers
checks = {
    "PHÂN TÍCH VẠN VẬT": "nghề gì / vạn vật block",
    "Khoảng": "tuổi block (age)",
    "SỐ LƯỢNG": "bao nhiêu block (count)",
    "KẾT LUẬN AI OFFLINE": "green box header",
}

print("\n--- MARKER CHECK ---")
for marker, desc in checks.items():
    found = marker in result
    status = "✅ FOUND" if found else "❌ MISSING"
    print(f"  {status}: '{marker}' ({desc})")

# Extract what appears in green box
print("\n--- GREEN BOX CONTENT ---")
# Find the green box div
green_match = re.search(
    r'KẾT LUẬN AI OFFLINE.*?<div[^>]*font-size:2em[^>]*>(.*?)</div>',
    result, re.DOTALL
)
if green_match:
    raw_answer = green_match.group(1)
    clean = re.sub(r'<[^>]+>', ' ', raw_answer).strip()
    print(f"  Raw green box answer: {clean[:500]}")
    
    # Count how many answers are in there
    answers = [a.strip() for a in clean.split('<br>') if a.strip()]
    if not answers or len(answers) <= 1:
        # Try splitting by newline
        answers = [a.strip() for a in clean.split('\n') if a.strip()]
    print(f"  Number of distinct answers: {len(answers)}")
    for i, a in enumerate(answers):
        print(f"    [{i+1}] {a[:200]}")
else:
    print("  ❌ Could not find green box content!")

# Check for "CÂU TRẢ LỜI:" text that should be stripped
if "CÂU TRẢ LỜI:" in result:
    count = result.count("CÂU TRẢ LỜI:")
    print(f"\n⚠️ Found {count} occurrences of 'CÂU TRẢ LỜI:' in output")
    # Find in green box specifically
    if green_match and "CÂU TRẢ LỜI:" in green_match.group(1):
        print("  ❌ 'CÂU TRẢ LỜI:' appears IN THE GREEN BOX - should be stripped!")
    else:
        print("  ℹ️ 'CÂU TRẢ LỜI:' only in detail sections (OK)")

print("\n" + "=" * 80)
print("TEST COMPLETE")
