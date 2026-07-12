"""
FORTUNE CALENDAR AI - Lịch Vận Hạn
Theo dõi vận hạn theo tháng, năm
"""

from datetime import datetime
from zoneinfo import ZoneInfo

VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")

VAN_HAN = {
    1: {"ten": "Thái Tuế", "muc": "cao", "luu_y": "Năm đặc biệt, cẩn thận"},
    2: {"ten": "Thiên Đức", "muc": "thấp", "luu_y": "Có quý nhân phù hộ"},
    3: {"ten": "Tam Tai", "muc": "cao", "luu_y": "3 năm hạn, cẩn thận"},
    4: {"ten": "Tứ Hành", "muc": "trung", "luu_y": "Di chuyển cẩn thận"},
    5: {"ten": "Hoàng Ân", "muc": "thấp", "luu_y": "Năm may mắn"},
}


class FortuneCalendarAI:
    def __init__(self):
        pass
    
    def get_year_fortune(self, nam_sinh, nam_xem=None):
        if nam_xem is None:
            nam_xem = datetime.now(VN_TZ).year
        
        tuoi = nam_xem - nam_sinh
        index = tuoi % 5 + 1
        van = VAN_HAN.get(index, VAN_HAN[1])
        
        return {
            "nam_xem": nam_xem,
            "tuoi": tuoi,
            "van_han": van["ten"],
            "muc_do": van["muc"],
            "luu_y": van["luu_y"]
        }
    
    def get_month_fortune(self, thang=None):
        if thang is None:
            thang = datetime.now(VN_TZ).month
        
        score = 50 + (thang % 3) * 10
        if thang in [1, 4, 7, 10]:
            note = "Tháng tốt để khởi sự"
        elif thang in [2, 5, 8, 11]:
            note = "Tháng ổn định"
        else:
            note = "Tháng cẩn thận"
        
        return {"thang": thang, "diem": score, "ghi_chu": note}
    
    def get_report(self, nam_sinh):
        year = self.get_year_fortune(nam_sinh)
        month = self.get_month_fortune()
        
        output = ["## 📅 LỊCH VẬN HẠN"]
        output.append(f"\n### Năm {year['nam_xem']}")
        output.append(f"- Tuổi: {year['tuoi']}")
        output.append(f"- Vận hạn: **{year['van_han']}**")
        output.append(f"- Mức độ: {year['muc_do']}")
        output.append(f"- Lưu ý: {year['luu_y']}")
        output.append(f"\n### Tháng {month['thang']}")
        output.append(f"- Điểm: {month['diem']}/100")
        output.append(f"- {month['ghi_chu']}")
        return "\n".join(output)


_ai = None
def get_fortune_calendar():
    global _ai
    if _ai is None: _ai = FortuneCalendarAI()
    return _ai
