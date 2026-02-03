"""
DATE SELECTOR AI - Chọn Ngày Tốt
Tìm ngày tốt cho các sự kiện quan trọng
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")

# Can Chi
CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

# Ngày tốt theo việc
NGAY_TOT = {
    "ket_hon": ["Giáp Tý", "Giáp Thìn", "Ất Sửu", "Bính Dần", "Đinh Mão"],
    "khai_truong": ["Giáp Tý", "Ất Mão", "Bính Ngọ", "Kỷ Dậu"],
    "dong_tho": ["Giáp Tý", "Kỷ Mùi", "Canh Thân", "Tân Dậu"],
    "xuat_hanh": ["Giáp Dần", "Ất Mão", "Bính Ngọ", "Đinh Tỵ"],
    "an_tang": ["Canh Thân", "Tân Dậu", "Nhâm Tuất", "Quý Hợi"],
    "nhap_trach": ["Giáp Tý", "Ất Sửu", "Bính Dần", "Đinh Mão"],
    "ky_hop_dong": ["Giáp Tý", "Ất Sửu", "Canh Thân", "Tân Dậu"],
}

# Ngày cần tránh
NGAY_XAU = {
    "tam_nuong": [3, 7, 13, 18, 22, 27],  # Ngày âm
    "sat_chu": [5, 14, 23],  # Ngày âm
    "hoang_oc": [1, 10, 19, 28],  # Ngày dương đặc biệt tránh nhập trạch
}


class DateSelectorAI:
    """
    AI Chọn ngày tốt
    - Tìm ngày tốt cho các sự kiện
    - Tránh ngày xấu
    - Đề xuất thời điểm phù hợp
    """
    
    def __init__(self):
        pass
    
    def get_can_chi_ngay(self, date=None):
        """Tính Can Chi của ngày"""
        if date is None:
            date = datetime.now(VN_TZ)
        
        base = datetime(2024, 1, 1, tzinfo=VN_TZ)  # Ngày Giáp Tý
        delta = (date - base).days
        
        can_index = delta % 10
        chi_index = delta % 12
        
        return f"{CAN[can_index]} {CHI[chi_index]}"
    
    def find_good_dates(self, event_type, start_date=None, days_ahead=30):
        """Tìm các ngày tốt trong khoảng thời gian"""
        if start_date is None:
            start_date = datetime.now(VN_TZ)
        
        # Xác định loại sự kiện
        event_lower = event_type.lower()
        if any(kw in event_lower for kw in ["cưới", "hôn"]):
            event_key = "ket_hon"
        elif any(kw in event_lower for kw in ["khai", "mở"]):
            event_key = "khai_truong"
        elif any(kw in event_lower for kw in ["động", "xây"]):
            event_key = "dong_tho"
        elif any(kw in event_lower for kw in ["đi", "xuất"]):
            event_key = "xuat_hanh"
        elif any(kw in event_lower for kw in ["táng", "chôn"]):
            event_key = "an_tang"
        elif any(kw in event_lower for kw in ["nhà", "trạch"]):
            event_key = "nhap_trach"
        elif any(kw in event_lower for kw in ["ký", "hợp đồng"]):
            event_key = "ky_hop_dong"
        else:
            event_key = "khai_truong"  # Default
        
        good_can_chi = NGAY_TOT.get(event_key, [])
        good_dates = []
        
        for i in range(days_ahead):
            check_date = start_date + timedelta(days=i)
            can_chi = self.get_can_chi_ngay(check_date)
            
            # Kiểm tra ngày tốt
            is_good = any(gc in can_chi for gc in good_can_chi)
            
            # Kiểm tra không phải ngày xấu
            day_of_month = check_date.day
            is_bad = any(
                day_of_month in bad_days 
                for bad_days in NGAY_XAU.values()
            )
            
            if is_good and not is_bad:
                good_dates.append({
                    "date": check_date.strftime("%d/%m/%Y"),
                    "weekday": self._get_weekday_vn(check_date.weekday()),
                    "can_chi": can_chi,
                    "score": 90 if is_good else 70
                })
        
        return good_dates[:5]  # Trả về 5 ngày tốt nhất
    
    def _get_weekday_vn(self, weekday):
        """Chuyển đổi ngày trong tuần sang tiếng Việt"""
        days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
        return days[weekday]
    
    def check_specific_date(self, date, event_type="Chung"):
        """Kiểm tra một ngày cụ thể"""
        can_chi = self.get_can_chi_ngay(date)
        day_of_month = date.day
        weekday = self._get_weekday_vn(date.weekday())
        
        # Đánh giá
        score = 50
        notes = []
        
        # Kiểm tra Can Chi tốt
        for event, good_days in NGAY_TOT.items():
            if any(gc in can_chi for gc in good_days):
                score += 20
                notes.append(f"✅ Ngày tốt cho {event}")
                break
        
        # Kiểm tra ngày xấu
        if day_of_month in NGAY_XAU.get("tam_nuong", []):
            score -= 30
            notes.append("⚠️ Ngày Tam Nương - Tránh việc lớn")
        
        if day_of_month in NGAY_XAU.get("sat_chu", []):
            score -= 20
            notes.append("⚠️ Ngày Sát Chủ - Cẩn thận")
        
        # Điểm theo ngày trong tuần
        if date.weekday() in [5, 6]:  # Thứ 7, Chủ nhật
            score += 5
            notes.append("📅 Cuối tuần, thuận tiện")
        
        score = max(0, min(100, score))
        
        return {
            "date": date.strftime("%d/%m/%Y"),
            "weekday": weekday,
            "can_chi": can_chi,
            "score": score,
            "verdict": self._score_to_verdict(score),
            "notes": notes
        }
    
    def _score_to_verdict(self, score):
        """Chuyển điểm thành đánh giá"""
        if score >= 80:
            return "RẤT TỐT - Ngày hoàng đạo"
        elif score >= 60:
            return "TỐT - Có thể tiến hành"
        elif score >= 40:
            return "TRUNG BÌNH - Cân nhắc"
        else:
            return "XẤU - Nên tránh"
    
    def get_month_overview(self, month=None, year=None):
        """Tổng quan ngày tốt/xấu trong tháng"""
        now = datetime.now(VN_TZ)
        month = month or now.month
        year = year or now.year
        
        from calendar import monthrange
        days_in_month = monthrange(year, month)[1]
        
        good_days = []
        bad_days = []
        
        for day in range(1, days_in_month + 1):
            date = datetime(year, month, day, tzinfo=VN_TZ)
            result = self.check_specific_date(date)
            
            if result["score"] >= 70:
                good_days.append(f"{day} ({result['weekday']})")
            elif result["score"] <= 30:
                bad_days.append(f"{day} ({result['weekday']})")
        
        return {
            "thang": f"{month}/{year}",
            "ngay_tot": good_days[:10],
            "ngay_xau": bad_days[:5],
            "tong_ket": f"Có {len(good_days)} ngày tốt, {len(bad_days)} ngày cần tránh"
        }
    
    def get_date_recommendation(self, event_type):
        """Lấy khuyến nghị ngày tốt"""
        good_dates = self.find_good_dates(event_type)
        
        output = []
        output.append(f"## 📅 NGÀY TỐT CHO: {event_type.upper()}")
        output.append("")
        
        if good_dates:
            output.append("### Các ngày được khuyên dùng:")
            for i, date in enumerate(good_dates, 1):
                output.append(f"{i}. **{date['date']}** ({date['weekday']}) - {date['can_chi']}")
        else:
            output.append("Không tìm thấy ngày tốt trong 30 ngày tới.")
            output.append("Hãy thử tìm trong khoảng thời gian dài hơn.")
        
        output.append("")
        output.append("### Lưu ý:")
        output.append("- Nên chọn giờ Hoàng Đạo trong ngày đã chọn")
        output.append("- Tránh các ngày Tam Nương (3, 7, 13, 18, 22, 27 âm lịch)")
        
        return "\n".join(output)


# Singleton
_selector = None

def get_date_selector():
    global _selector
    if _selector is None:
        _selector = DateSelectorAI()
    return _selector


if __name__ == "__main__":
    selector = get_date_selector()
    
    print(selector.get_date_recommendation("Kết hôn"))
    print("\n" + "="*50 + "\n")
    
    today = datetime.now(VN_TZ)
    print(f"Kiểm tra ngày hôm nay:")
    result = selector.check_specific_date(today)
    print(f"- Ngày: {result['date']}")
    print(f"- Can Chi: {result['can_chi']}")
    print(f"- Đánh giá: {result['verdict']}")
