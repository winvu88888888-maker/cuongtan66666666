"""
Placeholder for integrated_knowledge_base
Provides fallback functions for missing knowledge base modules
"""

def get_comprehensive_palace_info(palace_num):
    """Fallback for missing palace info"""
    return {
        "name": f"Cung {palace_num}",
        "element": "N/A",
        "star": "N/A",
        "door": "N/A",
        "deity": "N/A",
        "stem_heaven": "N/A",
        "stem_earth": "N/A",
        "star_desc": "Dữ liệu đang được đồng bộ...",
        "door_desc": "Dữ liệu đang được đồng bộ...",
        "deity_desc": "Dữ liệu đang được đồng bộ...",
        "is_kong_wang": False,
        "is_di_ma": False
    }

def format_info_for_display(info):
    return str(info)

def get_qua_info(qua_name):
    return {"name": qua_name, "desc": "Thông tin đang cập nhật..."}

def get_sao_info(sao_name):
    return {"name": sao_name, "desc": "Thông tin đang cập nhật..."}

def get_mon_info(mon_name):
    return {"name": mon_name, "desc": "Thông tin đang cập nhật..."}

def get_can_info(can_name):
    return {"name": can_name, "desc": "Thông tin đang cập nhật..."}
