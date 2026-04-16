import sys
sys.path.insert(0, r'C:\Users\GHC\.gemini\antigravity\scratch\cuongtan66666666_fix')
from interaction_diagrams import split_compound_question, format_parsed_questions

tests = [
    "bố tôi bị bệnh nặng hay không và khi nào sẽ khỏi?",
    "tôi có nên đầu tư không, khi nào sẽ có lãi, và rủi ro thế nào?",
    "vợ tôi có ngoại tình không?",
    "con trai tôi thi có đỗ không và bao giờ có kết quả?",
    "tôi mất điện thoại ở đâu, có tìm được không?",
    "năm nay tài chính thế nào, sức khỏe ra sao, và tình cảm có thuận lợi không?",
]

for q in tests:
    pqs = split_compound_question(q)
    print(f"\n{'='*60}")
    print(f"INPUT: {q}")
    print(f"TÁCH: {len(pqs)} câu")
    for pq in pqs:
        person = pq.get('person', '-') or '-'
        print(f"  [{pq['index']}] \"{pq['text']}\"")
        print(f"      Person={person} | DT={pq['dung_than']} | Type={pq['qtype']} | Topic={pq['topic']} | Diagram={pq['diagram_id']}")
    
    if len(pqs) > 1:
        print(format_parsed_questions(pqs))
