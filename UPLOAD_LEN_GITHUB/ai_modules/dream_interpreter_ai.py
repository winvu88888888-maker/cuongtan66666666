"""
DREAM INTERPRETER AI - Giải Mộng
Phân tích và giải thích giấc mơ
"""

DREAMS = {
    "nuoc": {"tuong": "Thủy", "tot": "Tiền tài đến", "xau": "Khó khăn", "so": [1, 6]},
    "lua": {"tuong": "Hỏa", "tot": "Đam mê", "xau": "Xung đột", "so": [2, 7]},
    "ran": {"tuong": "Tiểu nhân", "tot": "Thoát nạn", "xau": "Bị hại", "so": [4, 9]},
    "tien": {"tuong": "Tài", "tot": "Thu nhập", "xau": "Mất tiền", "so": [2, 8]},
    "bay": {"tuong": "Thăng tiến", "tot": "Thành công", "xau": "Thất bại", "so": [1, 9]},
    "cho": {"tuong": "Bạn bè", "tot": "Có người giúp", "xau": "Bị phản", "so": [1, 8]},
    "meo": {"tuong": "Phụ nữ", "tot": "Quý nhân nữ", "xau": "Tiểu nhân", "so": [4, 7]},
    "nguoi_chet": {"tuong": "Tổ tiên", "tot": "Được phù hộ", "xau": "Cần cúng", "so": [5, 0]},
}


class DreamInterpreterAI:
    def __init__(self):
        self.dreams = DREAMS
    
    def interpret(self, dream_desc):
        desc = dream_desc.lower()
        for key, data in self.dreams.items():
            if key in desc:
                return {
                    "chu_de": key, "tuong": data["tuong"],
                    "tot": data["tot"], "xau": data["xau"],
                    "so": data["so"]
                }
        return {"message": "Không tìm thấy", "so": []}
    
    def get_report(self, dream_desc):
        r = self.interpret(dream_desc)
        if "message" in r:
            return f"## 🌙 GIẢI MỘNG\n\n{r['message']}"
        return f"""## 🌙 GIẢI MỘNG
**Chủ đề:** {r['chu_de']}
**Tượng:** {r['tuong']}
**Điềm tốt:** {r['tot']}
**Điềm xấu:** {r['xau']}
**Số may:** {r['so']}"""


_ai = None
def get_dream_interpreter():
    global _ai
    if _ai is None: _ai = DreamInterpreterAI()
    return _ai
