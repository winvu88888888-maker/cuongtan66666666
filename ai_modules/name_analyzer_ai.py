"""
NAME ANALYZER AI - Phân Tích Tên
Phân tích ý nghĩa và ngũ hành của tên
"""

NGU_HANH_BO = {
    "Thủy": ["氵", "冫", "水"],
    "Mộc": ["木", "艹", "卄"],
    "Hỏa": ["火", "灬", "日"],
    "Thổ": ["土", "山", "石"],
    "Kim": ["金", "钅", "釒"]
}

Y_NGHIA = {
    "an": "Bình an", "bình": "Yên bình", "cường": "Mạnh mẽ",
    "dũng": "Dũng cảm", "đức": "Đức độ", "hạnh": "Hạnh phúc",
    "hiếu": "Hiếu thảo", "hùng": "Anh hùng", "khang": "Khỏe mạnh",
    "long": "Rồng", "minh": "Sáng suốt", "phúc": "Phúc lành",
    "quang": "Sáng", "tài": "Tài năng", "thành": "Thành công",
    "trí": "Trí tuệ", "vinh": "Vinh hiển", "vũ": "Vũ trụ"
}


class NameAnalyzerAI:
    def __init__(self):
        pass
    
    def analyze(self, name):
        name_lower = name.lower()
        found = []
        for key, meaning in Y_NGHIA.items():
            if key in name_lower:
                found.append(f"{key}: {meaning}")
        
        total = sum(ord(c) for c in name)
        hanh_index = total % 5
        hanh = ["Mộc", "Hỏa", "Thổ", "Kim", "Thủy"][hanh_index]
        
        return {
            "ten": name,
            "ngu_hanh": hanh,
            "y_nghia": found if found else ["Không tìm thấy ý nghĩa đặc biệt"],
            "so_linh": total % 9 + 1
        }
    
    def get_report(self, name):
        r = self.analyze(name)
        output = [f"## 📛 PHÂN TÍCH TÊN: {r['ten']}"]
        output.append(f"**Ngũ hành:** {r['ngu_hanh']}")
        output.append(f"**Số linh:** {r['so_linh']}")
        output.append("**Ý nghĩa:**")
        for y in r['y_nghia']:
            output.append(f"- {y}")
        return "\n".join(output)


_ai = None
def get_name_analyzer():
    global _ai
    if _ai is None: _ai = NameAnalyzerAI()
    return _ai
