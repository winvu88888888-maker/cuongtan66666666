"""
FENG SHUI AI - Tư Vấn Phong Thủy
Phân tích và tư vấn phong thủy nhà cửa, văn phòng
"""

HUONG_NHA = {
    "Bắc": {"hanh": "Thủy", "mau": ["Đen", "Xanh dương"], "tranh": "Đỏ, Cam"},
    "Nam": {"hanh": "Hỏa", "mau": ["Đỏ", "Hồng"], "tranh": "Đen, Xanh dương"},
    "Đông": {"hanh": "Mộc", "mau": ["Xanh lá"], "tranh": "Trắng, Kim loại"},
    "Tây": {"hanh": "Kim", "mau": ["Trắng", "Bạc"], "tranh": "Đỏ"},
    "Đông Bắc": {"hanh": "Thổ", "mau": ["Vàng", "Nâu"], "tranh": "Xanh lá"},
    "Đông Nam": {"hanh": "Mộc", "mau": ["Xanh lá"], "tranh": "Trắng"},
    "Tây Bắc": {"hanh": "Kim", "mau": ["Trắng"], "tranh": "Đỏ"},
    "Tây Nam": {"hanh": "Thổ", "mau": ["Vàng"], "tranh": "Xanh lá"}
}

MENH = {
    1: "Khảm", 2: "Khôn", 3: "Chấn", 4: "Tốn",
    5: "Trung Cung", 6: "Càn", 7: "Đoài", 8: "Cấn", 9: "Ly"
}


class FengShuiAI:
    def __init__(self):
        pass
    
    def tinh_menh(self, nam_sinh, gioi_tinh):
        nam = int(nam_sinh)
        if gioi_tinh.lower() in ["nam", "male"]:
            so = (100 - (nam % 100)) % 9
        else:
            so = ((nam % 100) - 4) % 9
        return MENH.get(so if so else 5, "Trung Cung")
    
    def phan_tich_huong(self, huong):
        data = HUONG_NHA.get(huong, {})
        return {
            "huong": huong,
            "hanh": data.get("hanh", ""),
            "mau_tot": data.get("mau", []),
            "mau_tranh": data.get("tranh", "")
        }
    
    def get_report(self, huong_nha, nam_sinh=None, gioi_tinh=None):
        h = self.phan_tich_huong(huong_nha)
        output = [f"## 🏠 PHÂN TÍCH PHONG THỦY"]
        output.append(f"**Hướng nhà:** {h['huong']}")
        output.append(f"**Hành:** {h['hanh']}")
        output.append(f"**Màu tốt:** {', '.join(h['mau_tot'])}")
        output.append(f"**Màu tránh:** {h['mau_tranh']}")
        
        if nam_sinh and gioi_tinh:
            menh = self.tinh_menh(nam_sinh, gioi_tinh)
            output.append(f"\n**Mệnh chủ nhà:** {menh}")
        
        return "\n".join(output)


_ai = None
def get_feng_shui_ai():
    global _ai
    if _ai is None: _ai = FengShuiAI()
    return _ai
