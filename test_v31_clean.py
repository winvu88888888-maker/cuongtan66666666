import sys
sys.path.insert(0, r'C:\Users\GHC\.gemini\antigravity\scratch\cuongtan66666666_fix')
from interaction_diagrams import clean_question, split_compound_question

tests = [
    "xin hỏi ạ... bố tôi bệnh nặng hay không???!!! cảm ơn",
    "cho em hỏi chút ạ, tôi có nên đầu tư không nhỉ??? haha",
    "dạ thưa thầy, vợ tôi có ngoại tình không ạ...",
    "!!!??? tài chính năm nay thế nào ơi @@@###",
    "con trai tôi thi     đỗ     không...   và   bao giờ   có kết quả????",
    "làm ơn giúp tôi với ạ nhé, bố tôi bệnh nặng hay không, khi nào sẽ khỏi, và nên đi bệnh viện nào???",
    "haha ok bạn ơi tôi muốn hỏi sức khỏe tôi thế nào nhỉ lol",
    "~~~!!! mất điện thoại ở đâu nè, tìm được không hả???...",
]

for q in tests:
    cleaned = clean_question(q)
    pqs = split_compound_question(q)
    print(f"\nGOC: {q}")
    print(f"SACH: {cleaned}")
    print(f"TACH: {len(pqs)} cau")
    for pq in pqs:
        p = pq.get('person') or '-'
        print(f"  [{pq['index']}] \"{pq['text']}\" | {p}/{pq['dung_than']} | {pq['qtype']} | {pq['diagram_id']}")
