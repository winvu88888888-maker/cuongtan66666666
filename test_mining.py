import sys
import os
import json

# Add paths for local import
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'ai_modules'))

try:
    from shard_manager import add_entry, search_index
    print("✅ Hệ thống Lưu trữ Đa tầng: SẴN SÀNG")
    
    # Simulate a mining run
    print("🤖 Đang giả lập Quân đoàn AI đi khai thác Internet...")
    
    entries = [
        {
            "title": "Cập nhật Xu hướng AI 2026",
            "content": "Tổng hợp: Gemini 3.0 đã ra mắt với khả năng tự trị cao hơn. Các mô hình Agentic AI đang trở thành xu hướng chủ đạo trong phát triển phần mềm toàn cầu.",
            "cat": "Kiến Thức",
            "source": "AI Miner: Tech Envoy"
        },
        {
            "title": "Nghiên cứu Kỳ Môn trong Kinh Doanh",
            "content": "Dữ liệu mới: Cách áp dụng 8 Cửa (Bát Môn) để chọn thời điểm ra mắt sản phẩm. Khai Môn luôn là lựa chọn hàng đầu cho khởi sự.",
            "cat": "Kỳ Môn Độn Giáp",
            "source": "AI Sage: Strategy Miner"
        }
    ]
    
    for e in entries:
        id = add_entry(e['title'], e['content'], e['cat'], e['source'], ["mining_test", "internet_data"])
        if id:
            print(f"  + Đã nạp: {e['title']} [ID: {id}]")
            
    print("\n🚀 KẾT QUẢ: Hệ thống đã thông suốt!")
    print(f"Hiện tại trong Kho Vô Tận đang có {len(search_index())} mục dữ liệu thực tế.")
    print("Bây giờ bạn hãy chạy sync_and_push.bat để đưa dữ liệu mẫu này lên Web.")

except Exception as e:
    print(f"❌ Lỗi: {e}")
