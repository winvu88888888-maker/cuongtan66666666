"""
SCHEDULER AI - Chọn Giờ Tốt Tự Động
Tính toán và đề xuất giờ tốt nhất để hành động
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Timezone Vietnam
VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")

# 12 Chi và giờ tương ứng
CHI_GIO = {
    "Tý": (23, 1), "Sửu": (1, 3), "Dần": (3, 5), "Mão": (5, 7),
    "Thìn": (7, 9), "Tỵ": (9, 11), "Ngọ": (11, 13), "Mùi": (13, 15),
    "Thân": (15, 17), "Dậu": (17, 19), "Tuất": (19, 21), "Hợi": (21, 23)
}

# Giờ Hoàng Đạo cố định theo Can ngày
HOANG_DAO_BY_CAN = {
    "Giáp": ["Tý", "Sửu", "Mão", "Ngọ", "Mùi", "Dậu"],
    "Kỷ": ["Tý", "Sửu", "Mão", "Ngọ", "Mùi", "Dậu"],
    "Ất": ["Dần", "Mão", "Tỵ", "Thân", "Dậu", "Hợi"],
    "Canh": ["Dần", "Mão", "Tỵ", "Thân", "Dậu", "Hợi"],
    "Bính": ["Thìn", "Tỵ", "Mùi", "Tuất", "Hợi", "Sửu"],
    "Tân": ["Thìn", "Tỵ", "Mùi", "Tuất", "Hợi", "Sửu"],
    "Đinh": ["Tý", "Dần", "Mão", "Ngọ", "Thân", "Dậu"],
    "Nhâm": ["Tý", "Dần", "Mão", "Ngọ", "Thân", "Dậu"],
    "Mậu": ["Sửu", "Thìn", "Tỵ", "Mùi", "Tuất", "Hợi"],
    "Quý": ["Sửu", "Thìn", "Tỵ", "Mùi", "Tuất", "Hợi"]
}

# Giờ Hắc Đạo (xấu)
HAC_DAO_BY_CAN = {
    "Giáp": ["Dần", "Thìn", "Tỵ", "Thân", "Tuất", "Hợi"],
    "Kỷ": ["Dần", "Thìn", "Tỵ", "Thân", "Tuất", "Hợi"],
    "Ất": ["Tý", "Sửu", "Thìn", "Ngọ", "Mùi", "Tuất"],
    "Canh": ["Tý", "Sửu", "Thìn", "Ngọ", "Mùi", "Tuất"],
    "Bính": ["Tý", "Dần", "Mão", "Ngọ", "Thân", "Dậu"],
    "Tân": ["Tý", "Dần", "Mão", "Ngọ", "Thân", "Dậu"],
    "Đinh": ["Sửu", "Thìn", "Tỵ", "Mùi", "Tuất", "Hợi"],
    "Nhâm": ["Sửu", "Thìn", "Tỵ", "Mùi", "Tuất", "Hợi"],
    "Mậu": ["Tý", "Dần", "Mão", "Ngọ", "Thân", "Dậu"],
    "Quý": ["Tý", "Dần", "Mão", "Ngọ", "Thân", "Dậu"]
}

# Giờ tốt theo loại việc
GIO_TOT_THEO_VIEC = {
    "kinh_doanh": ["Mão", "Tỵ", "Ngọ", "Thân"],
    "giao_dich": ["Thìn", "Tỵ", "Mùi", "Thân"],
    "ky_hop_dong": ["Mão", "Ngọ", "Dậu"],
    "xuat_hanh": ["Dần", "Mão", "Ngọ", "Thân"],
    "cau_tai": ["Thìn", "Tỵ", "Mùi"],
    "khai_truong": ["Mão", "Thìn", "Ngọ", "Dậu"],
    "hon_nhan": ["Mão", "Ngọ", "Dậu"],
    "xin_viec": ["Mão", "Tỵ", "Thân"],
    "hoc_tap": ["Dần", "Mão", "Tỵ"],
    "chua_benh": ["Dần", "Tỵ", "Thân", "Dậu"],
    "xay_dung": ["Dần", "Mão", "Thìn", "Ngọ"],
    "dat_dai": ["Thìn", "Tỵ", "Mùi", "Tuất"]
}


class SchedulerAI:
    """
    AI Chọn Giờ Tốt Tự Động
    Tính toán giờ Hoàng Đạo, giờ tốt theo chủ đề
    """
    
    def __init__(self):
        self.vn_tz = VN_TZ
    
    def get_current_hour_chi(self):
        """Lấy Chi của giờ hiện tại"""
        now = datetime.now(self.vn_tz)
        hour = now.hour
        
        for chi, (start, end) in CHI_GIO.items():
            if start <= hour < end or (chi == "Tý" and (hour >= 23 or hour < 1)):
                return chi, now
        
        return "Tý", now
    
    def get_can_ngay(self, date=None):
        """Tính Can của ngày (simplified - cần bảng tra chính xác)"""
        if date is None:
            date = datetime.now(self.vn_tz)
        
        # Công thức đơn giản hóa
        CAN_10 = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
        
        # Base date: 2024-01-01 là ngày Giáp Tý
        base = datetime(2024, 1, 1, tzinfo=self.vn_tz)
        delta = (date - base).days
        
        can_index = delta % 10
        return CAN_10[can_index]
    
    def get_hoang_dao_hours(self, can_ngay=None):
        """Lấy các giờ Hoàng Đạo trong ngày"""
        if can_ngay is None:
            can_ngay = self.get_can_ngay()
        
        hoang_dao = HOANG_DAO_BY_CAN.get(can_ngay, [])
        
        result = []
        for chi in hoang_dao:
            start, end = CHI_GIO[chi]
            result.append({
                "chi": chi,
                "gio_bat_dau": f"{start:02d}:00",
                "gio_ket_thuc": f"{end:02d}:00",
                "loai": "Hoàng Đạo (Tốt)"
            })
        
        return result
    
    def get_hac_dao_hours(self, can_ngay=None):
        """Lấy các giờ Hắc Đạo (xấu) trong ngày"""
        if can_ngay is None:
            can_ngay = self.get_can_ngay()
        
        hac_dao = HAC_DAO_BY_CAN.get(can_ngay, [])
        
        result = []
        for chi in hac_dao:
            start, end = CHI_GIO[chi]
            result.append({
                "chi": chi,
                "gio_bat_dau": f"{start:02d}:00",
                "gio_ket_thuc": f"{end:02d}:00",
                "loai": "Hắc Đạo (Xấu)"
            })
        
        return result
    
    def find_best_hours_for_topic(self, topic):
        """Tìm giờ tốt nhất cho chủ đề cụ thể"""
        topic_lower = topic.lower()
        
        # Xác định loại việc
        viec_type = "chung"
        for key in GIO_TOT_THEO_VIEC:
            if key.replace("_", " ") in topic_lower or key in topic_lower:
                viec_type = key
                break
        
        # Mapping thêm
        if any(kw in topic_lower for kw in ["tiền", "tài", "lương", "đầu tư"]):
            viec_type = "cau_tai"
        elif any(kw in topic_lower for kw in ["việc", "công việc", "xin việc"]):
            viec_type = "xin_viec"
        elif any(kw in topic_lower for kw in ["đi", "xuất hành", "du lịch"]):
            viec_type = "xuat_hanh"
        elif any(kw in topic_lower for kw in ["hợp đồng", "ký"]):
            viec_type = "ky_hop_dong"
        elif any(kw in topic_lower for kw in ["kinh doanh", "buôn bán", "mở"]):
            viec_type = "kinh_doanh"
        elif any(kw in topic_lower for kw in ["cưới", "hôn", "tình"]):
            viec_type = "hon_nhan"
        elif any(kw in topic_lower for kw in ["bệnh", "khám", "chữa"]):
            viec_type = "chua_benh"
        elif any(kw in topic_lower for kw in ["học", "thi"]):
            viec_type = "hoc_tap"
        elif any(kw in topic_lower for kw in ["nhà", "xây", "đất"]):
            viec_type = "dat_dai"
        
        # Lấy giờ tốt theo loại việc
        gio_tot_viec = GIO_TOT_THEO_VIEC.get(viec_type, [])
        
        # Kết hợp với giờ Hoàng Đạo
        can_ngay = self.get_can_ngay()
        hoang_dao = HOANG_DAO_BY_CAN.get(can_ngay, [])
        
        # Ưu tiên: Giờ vừa Hoàng Đạo vừa tốt cho việc
        best_hours = []
        good_hours = []
        
        for chi in gio_tot_viec:
            start, end = CHI_GIO[chi]
            hour_info = {
                "chi": chi,
                "gio": f"{start:02d}:00 - {end:02d}:00",
                "loai_viec": viec_type
            }
            
            if chi in hoang_dao:
                hour_info["xep_hang"] = "⭐⭐⭐ TỐT NHẤT (Hoàng Đạo + Hợp việc)"
                best_hours.append(hour_info)
            else:
                hour_info["xep_hang"] = "⭐⭐ TỐT (Hợp việc)"
                good_hours.append(hour_info)
        
        return {
            "can_ngay": can_ngay,
            "loai_viec": viec_type,
            "gio_tot_nhat": best_hours,
            "gio_tot": good_hours,
            "tong_hop": best_hours + good_hours
        }
    
    def get_next_good_hour(self, topic=None):
        """Lấy giờ tốt tiếp theo từ bây giờ"""
        now = datetime.now(self.vn_tz)
        current_hour = now.hour
        
        can_ngay = self.get_can_ngay()
        
        if topic:
            hours_info = self.find_best_hours_for_topic(topic)
            all_good_hours = hours_info["tong_hop"]
        else:
            hoang_dao = self.get_hoang_dao_hours(can_ngay)
            all_good_hours = hoang_dao
        
        # Tìm giờ tốt tiếp theo
        for hour_info in all_good_hours:
            chi = hour_info["chi"]
            start, end = CHI_GIO[chi]
            
            # Nếu giờ tốt chưa đến
            if start > current_hour:
                hour_info["con_lai"] = f"{start - current_hour} giờ nữa"
                return hour_info
        
        # Nếu hết giờ tốt hôm nay -> ngày mai
        return {
            "chi": all_good_hours[0]["chi"] if all_good_hours else "Mão",
            "gio": "Ngày mai",
            "note": "Giờ tốt tiếp theo là ngày mai"
        }
    
    def get_full_schedule(self, topic=None):
        """Lấy lịch trình đầy đủ trong ngày"""
        now = datetime.now(self.vn_tz)
        can_ngay = self.get_can_ngay()
        
        output = []
        output.append(f"## 📅 LỊCH GIỜ TỐT - {now.strftime('%d/%m/%Y')}")
        output.append(f"**Can ngày:** {can_ngay}")
        output.append("")
        
        # Giờ tốt nhất cho chủ đề
        if topic:
            output.append(f"### 🎯 GIỜ TỐT CHO: {topic.upper()}")
            hours = self.find_best_hours_for_topic(topic)
            
            if hours["gio_tot_nhat"]:
                output.append("**Giờ tốt nhất:**")
                for h in hours["gio_tot_nhat"]:
                    output.append(f"- {h['chi']} ({h['gio']}) - {h['xep_hang']}")
            
            if hours["gio_tot"]:
                output.append("\n**Giờ tốt:**")
                for h in hours["gio_tot"]:
                    output.append(f"- {h['chi']} ({h['gio']}) - {h['xep_hang']}")
            
            output.append("")
        
        # Giờ Hoàng Đạo
        output.append("### ✨ GIỜ HOÀNG ĐẠO (TỐT)")
        hoang_dao = self.get_hoang_dao_hours(can_ngay)
        for h in hoang_dao:
            output.append(f"- {h['chi']}: {h['gio_bat_dau']} - {h['gio_ket_thuc']}")
        
        output.append("")
        
        # Giờ Hắc Đạo
        output.append("### ⚫ GIỜ HẮC ĐẠO (TRÁNH)")
        hac_dao = self.get_hac_dao_hours(can_ngay)
        for h in hac_dao:
            output.append(f"- {h['chi']}: {h['gio_bat_dau']} - {h['gio_ket_thuc']}")
        
        # Giờ tốt tiếp theo
        output.append("")
        output.append("### ⏰ GIỜ TỐT TIẾP THEO")
        next_good = self.get_next_good_hour(topic)
        if "con_lai" in next_good:
            output.append(f"**{next_good['chi']}** - còn {next_good['con_lai']}")
        else:
            output.append(f"**{next_good.get('note', 'Không xác định')}**")
        
        return "\n".join(output)


# Singleton
_scheduler = None

def get_scheduler():
    global _scheduler
    if _scheduler is None:
        _scheduler = SchedulerAI()
    return _scheduler


if __name__ == "__main__":
    scheduler = get_scheduler()
    
    print("=== TEST SCHEDULER AI ===\n")
    print(scheduler.get_full_schedule("Xin việc"))
