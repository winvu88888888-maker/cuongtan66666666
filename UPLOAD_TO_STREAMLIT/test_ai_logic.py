import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from free_ai_helper import FreeAIHelper
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(1)

def run_tests():
    ai = FreeAIHelper()
    
    mock_lh_data = {
        'chi_ngay': 'Tý', 'chi_thang': 'Ngọ', 
        'ban': {'2': {'chi': 'Mão', 'hoa': 'Dần'}},
        'dong_hao': [2],
        'v23_factors': ['Tuần Không']
    }
    
    print("="*60)
    print("🚀 BẮT ĐẦU CHẠY BÀI TEST TÒA ÁN AI V42.9.4")
    print("="*60)
    
    test_cases = [
        {
            "name": "1. Câu hỏi kép (Multi-Intent)",
            "q": "Tôi đi xin việc có đỗ không và mẹ tôi đang ốm thì chừng nào khỏi bệnh?",
            "kwargs": {'luc_hao_data': mock_lh_data}
        },
        {
            "name": "2. Bypass Module: TỬ VI (Lá số trọn đời)",
            "q": "Lá số của tôi có giàu không?",
            "kwargs": {'tu_vi_data': {'cung_tai_bach': ['Vũ Khúc', 'Lộc Tồn']}}
        },
        {
            "name": "3. Bypass Module: XEM NGÀY ĐẸP (Trạch Cát)",
            "q": "Ngày mùng 5 tháng sau cưới vợ được không?",
            "kwargs": {'xem_ngay_data': {'hoang_dao': 'Thanh Long', 'truc': 'Mãn'}}
        }
    ]
    
    for tc in test_cases:
        print(f"\n{tc['name']}")
        print(f"❓ Câu hỏi: '{tc['q']}'")
        try:
            chart_data = {'nhan_ban': {'3': 'Sinh Môn'}, 'can_ngay': 'Giáp'}
            kwargs = tc.get('kwargs', {})
            
            output = ai.answer_question(
                tc['q'], 
                chart_data=chart_data, 
                luc_hao_data=kwargs.get('luc_hao_data'),
                tu_vi_data=kwargs.get('tu_vi_data'),
                xem_ngay_data=kwargs.get('xem_ngay_data')
            )
            
            print("-" * 40)
            print("🟢 OFFLINE REPORT (Dữ liệu gửi lên AI):")
            if output:
                print(output[:1000] + ("...\n[Đã cắt bớt]" if len(output) > 1000 else ""))
            else:
                print("No output generated.")
        except Exception as e:
            print(f"❌ LỖI: {e}")

if __name__ == "__main__":
    run_tests()
