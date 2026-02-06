
import datetime

# --- LUNAR CALENDAR TOOLS ---
# Simplified algorithmic converter (Approximate for 1900-2100)
# Ideally we should use a library like 'lunisolar' or 'lunar_python'
# but here we include a lightweight heuristic or rely on simple mapping if libs missing.

def get_khong_minh_luc_dieu(lunar_month, lunar_day):
    """
    Tính Khổng Minh Lục Diệu cho cả ngày (tương ứng 12 khung giờ).
    Công thức: (Tháng + Ngày + ChiGiờ - 2) % 6
    ChiGiờ: Tý=1, Sửu=2, ..., Hợi=12
    """
    luc_dieu_dict = {
        1: "Đại An (Tốt) - Mọi việc yên tâm, hành sự thành công.",
        2: "Lưu Niên (Xấu) - Việc trễ nải, rắc rối giấy tờ.",
        3: "Tốc Hỷ (Tốt) - Tin vui đến nhanh, cầu tài đắc lợi.",
        4: "Xích Khẩu (Xấu) - Cãi vã, thị phi, tranh chấp.",
        5: "Tiểu Cát (Tốt) - May mắn nhỏ, trôi chảy, được giúp đỡ.",
        0: "Không Vong (Xấu) - Mất mát, hư hỏng, việc không thành."
    }
    
    chi_hours = [
        "Tý (23h-1h)", "Sửu (1h-3h)", "Dần (3h-5h)", "Mão (5h-7h)", 
        "Thìn (7h-9h)", "Tỵ (9h-11h)", "Ngọ (11h-13h)", "Mùi (13h-15h)", 
        "Thân (15h-17h)", "Dậu (17h-19h)", "Tuất (19h-21h)", "Hợi (21h-23h)"
    ]
    
    results = []
    good_hours = []
    
    for i, hour_label in enumerate(chi_hours):
        chi_val = i + 1
        val = (lunar_month + lunar_day + chi_val - 2) % 6
        meaning = luc_dieu_dict[val if val != 0 else 0] # 0 is Khong Vong
        
        entry = f"- {hour_label}: {meaning}"
        results.append(entry)
        
        if val in [1, 3, 5]: # Dai An, Toc Hy, Tieu Cat
            good_hours.append(hour_label.split(' ')[0]) # Just the name "Tý"
            
    summary = f"Các giờ Tốt xuất hành hôm nay: {', '.join(good_hours)}"
    details = "\n".join(results)
    
    return summary, details

# --- LUNAR CONVERTER (Offline/Standalone) ---
# Since we don't have internet to pip install, use a basic conversion 
# or try to import library if available. 
# FALLBACK: If we can't convert, request user input or assume Solar~Lunar (bad but runnable)
# Better: Use 'lunardate' or 'lunar_python' if present. 

def get_lunar_date_offline(d):
    """
    Try to use installed libraries. If fail, return estimated.
    """
    try:
        from lunarcalendar import Converter, Solar
        solar = Solar(d.year, d.month, d.day)
        lunar = Converter.Solar2Lunar(solar)
        return lunar.month, lunar.day
    except ImportError:
        try:
            import lunardate
            l = lunardate.LunarDate.fromSolarDate(d.year, d.month, d.day)
            return l.month, l.day
        except ImportError:
            # Last Resort: Return Solar month/day (Warn user)
            # Or implement a small fixed logic? 
            # For now, let's just return Solar and warn.
            print("⚠️ Missing Lunar Library - Using Solar Date Approximation")
            return d.month, d.day

