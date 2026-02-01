"""
NOTIFICATION AI - Hệ Thống Cảnh Báo Thông Minh
Theo dõi và cảnh báo giờ tốt/xấu, sự kiện quan trọng
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")


# Giờ Hoàng Đạo theo Can ngày
HOANG_DAO = {
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

# Giờ theo Chi
CHI_GIO = {
    "Tý": (23, 1), "Sửu": (1, 3), "Dần": (3, 5), "Mão": (5, 7),
    "Thìn": (7, 9), "Tỵ": (9, 11), "Ngọ": (11, 13), "Mùi": (13, 15),
    "Thân": (15, 17), "Dậu": (17, 19), "Tuất": (19, 21), "Hợi": (21, 23)
}


class NotificationAI:
    """
    AI Hệ thống cảnh báo
    - Cảnh báo giờ tốt/xấu
    - Nhắc nhở sự kiện
    - Theo dõi lịch vận hạn
    """
    
    def __init__(self):
        self.pending_notifications = []
        self.notification_history = []
    
    def get_current_chi(self):
        """Lấy Chi của giờ hiện tại"""
        now = datetime.now(VN_TZ)
        hour = now.hour
        
        for chi, (start, end) in CHI_GIO.items():
            if chi == "Tý":
                if hour >= 23 or hour < 1:
                    return chi
            elif start <= hour < end:
                return chi
        return "Tý"
    
    def get_can_ngay(self, date=None):
        """Tính Can của ngày"""
        if date is None:
            date = datetime.now(VN_TZ)
        
        CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
        base = datetime(2024, 1, 1, tzinfo=VN_TZ)
        delta = (date - base).days
        return CAN[delta % 10]
    
    def check_current_hour(self):
        """Kiểm tra giờ hiện tại tốt hay xấu"""
        chi = self.get_current_chi()
        can = self.get_can_ngay()
        hoang_dao = HOANG_DAO.get(can, [])
        
        is_good = chi in hoang_dao
        
        return {
            "chi": chi,
            "can_ngay": can,
            "is_hoang_dao": is_good,
            "status": "✅ GIỜ HOÀNG ĐẠO - Tốt" if is_good else "⚫ GIỜ HẮC ĐẠO - Tránh việc lớn",
            "advice": "Giờ tốt để hành động" if is_good else "Nên chờ giờ tốt hơn"
        }
    
    def get_next_good_hour(self):
        """Lấy giờ Hoàng Đạo tiếp theo"""
        now = datetime.now(VN_TZ)
        hour = now.hour
        can = self.get_can_ngay()
        hoang_dao = HOANG_DAO.get(can, [])
        
        for chi in hoang_dao:
            start, end = CHI_GIO[chi]
            if chi == "Tý":
                if hour < 1 or hour >= 23:
                    continue
                if hour < 23:
                    return {"chi": chi, "gio": "23:00 - 01:00", "con_lai": f"{23 - hour} giờ"}
            elif start > hour:
                return {"chi": chi, "gio": f"{start:02d}:00 - {end:02d}:00", "con_lai": f"{start - hour} giờ"}
        
        # Ngày mai
        return {"chi": hoang_dao[0] if hoang_dao else "Mão", "gio": "Ngày mai", "con_lai": "Ngày mai"}
    
    def create_notification(self, message, notify_time, category="general"):
        """Tạo thông báo mới"""
        notification = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "message": message,
            "notify_time": notify_time,
            "category": category,
            "created_at": datetime.now().isoformat(),
            "sent": False
        }
        self.pending_notifications.append(notification)
        return notification["id"]
    
    def check_pending_notifications(self):
        """Kiểm tra các thông báo đến hạn"""
        now = datetime.now(VN_TZ)
        due_notifications = []
        
        for notif in self.pending_notifications:
            if not notif["sent"]:
                try:
                    notify_time = datetime.fromisoformat(notif["notify_time"])
                    if notify_time <= now:
                        due_notifications.append(notif)
                        notif["sent"] = True
                        self.notification_history.append(notif)
                except:
                    pass
        
        # Remove sent notifications
        self.pending_notifications = [n for n in self.pending_notifications if not n["sent"]]
        
        return due_notifications
    
    def get_daily_summary(self):
        """Lấy tóm tắt ngày"""
        now = datetime.now(VN_TZ)
        can = self.get_can_ngay()
        hoang_dao = HOANG_DAO.get(can, [])
        
        output = []
        output.append(f"## 📅 TÓM TẮT NGÀY {now.strftime('%d/%m/%Y')}")
        output.append("")
        output.append(f"**Can ngày:** {can}")
        output.append("")
        output.append("### ✅ Giờ Hoàng Đạo (Tốt):")
        for chi in hoang_dao:
            start, end = CHI_GIO[chi]
            output.append(f"- {chi}: {start:02d}:00 - {end:02d}:00")
        output.append("")
        
        # Current hour status
        current = self.check_current_hour()
        output.append(f"### 🕐 Giờ hiện tại: {current['chi']}")
        output.append(f"**{current['status']}**")
        output.append("")
        
        # Next good hour
        next_good = self.get_next_good_hour()
        output.append(f"### ⏰ Giờ tốt tiếp theo: {next_good['chi']} ({next_good.get('con_lai', '')})")
        
        return "\n".join(output)
    
    def get_important_dates(self, month=None, year=None):
        """Lấy các ngày quan trọng trong tháng"""
        now = datetime.now(VN_TZ)
        month = month or now.month
        year = year or now.year
        
        # Các ngày đặc biệt (simplified)
        special = {
            1: ["Mùng 1 Tết", "Mùng 7 - Khai hạ"],
            2: ["Rằm tháng Giêng", "Valentine"],
            3: ["8/3 - Quốc tế Phụ nữ"],
            5: ["1/5 - Lao động", "Mùng 5 - Tết Đoan Ngọ"],
            7: ["Rằm tháng 7 - Vu Lan"],
            8: ["Rằm Trung Thu"],
            9: ["2/9 - Quốc Khánh"],
            10: ["Rằm tháng 10"],
            11: ["20/11 - Nhà giáo VN"],
            12: ["Noel", "Tất niên"]
        }
        
        return {
            "thang": month,
            "nam": year,
            "ngay_dac_biet": special.get(month, ["Không có ngày đặc biệt"]),
            "luu_y": "Kiểm tra lịch âm để biết ngày Rằm, mùng 1"
        }
    
    def get_alerts(self):
        """Lấy tất cả cảnh báo hiện tại"""
        alerts = []
        
        # Check current hour
        current = self.check_current_hour()
        if not current["is_hoang_dao"]:
            alerts.append({
                "type": "hour_warning",
                "level": "warning",
                "message": f"⚫ Đang là giờ {current['chi']} (Hắc Đạo) - Tránh việc quan trọng"
            })
        else:
            alerts.append({
                "type": "hour_good",
                "level": "info",
                "message": f"✅ Đang là giờ {current['chi']} (Hoàng Đạo) - Tốt cho việc lớn"
            })
        
        # Add pending notifications
        due = self.check_pending_notifications()
        for n in due:
            alerts.append({
                "type": "notification",
                "level": "important",
                "message": n["message"]
            })
        
        return alerts


# Singleton
_notification = None

def get_notification_ai():
    global _notification
    if _notification is None:
        _notification = NotificationAI()
    return _notification


if __name__ == "__main__":
    ai = get_notification_ai()
    
    print(ai.get_daily_summary())
    print("\n" + "="*50 + "\n")
    
    alerts = ai.get_alerts()
    for alert in alerts:
        print(f"[{alert['level'].upper()}] {alert['message']}")
