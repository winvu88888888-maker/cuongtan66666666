from free_ai_helper import FreeAIHelper

def test_km_advanced():
    helper = FreeAIHelper()
    
    # Fake chart data and LH data to test the master diagram output
    chart_data = {
        'can_ngay': 'Giáp',
        'chi_ngay': 'Tý',
        'can_gio': 'Bính',
        'chi_gio': 'Dần',
        'is_duong_don': True,
        'cuc': 1,
        'can_thien_ban': {1: 'Bính', 2: 'Đinh'},
        'thien_ban': {1: 'Thiên Bồng', 2: 'Thiên Nhậm'},
        'nhan_ban': {1: 'Khai Môn', 2: 'Hưu Môn'},
        'than_ban': {1: 'Trực Phù', 2: 'Đằng Xà'},
        'dac_biet': ['Phản Ngâm']
    }
    
    # We simulate an answer process
    filled, info = helper._fill_master_diagram(
        question="Năm nay làm ăn thế nào?", 
        category_label="Tài Chính", 
        dung_than="Thê Tài", 
        hanh_dt="Thủy",
        unified_v22={'unified_pct': 80, 'tier_cap': 'VƯỢNG'},
        v23_lh_factors=[],
        chart_data=chart_data,
        luc_hao_data={}
    )
    
    print("----- MASTER DIAGRAM -----")
    print(filled)
    print("--------------------------")

if __name__ == "__main__":
    test_km_advanced()
