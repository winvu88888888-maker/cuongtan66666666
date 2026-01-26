import sys
import os
import time
import random

# Add paths for local import
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'ai_modules'))
sys.path.append(current_dir)

try:
    from shard_manager import add_entry
    from mining_strategist import MiningStrategist
    from maintenance_manager import MaintenanceManager
    from gemini_helper import GeminiQMDGHelper
    import streamlit as st
except ImportError:
    print("❌ Lỗi: Thiếu module cần thiết.")
    sys.exit(1)

def run_mining_cycle(api_key, category=None):
    """Executes one full cycle of autonomous mining."""
    if not api_key:
        print("⚠️ Thiếu API Key.")
        return
        
    strategist = MiningStrategist()
    ai_helper = GeminiQMDGHelper(api_key)
    
    # 1. Generate autonomous research queue
    queue = strategist.generate_research_queue(category, count=3)
    print(f"📡 Quân đoàn AI đã xác định mục tiêu khai thác: {queue}")
    
    for topic in queue:
        print(f"🤖 Đang khai thác sâu: {topic}...")
        
        # 2. Synthesize deep-dive content using Gemini
        mining_prompt = strategist.synthesize_mining_prompt(topic)
        content = ai_helper._call_ai(mining_prompt, use_hub=False) # Skip hub search to avoid circularity during mining
        
        # 3. Save to Sharded Hub
        cat_match = next((k for k in strategist.categories if any(t in topic for t in strategist.categories[k])), "Kiến Thức")
        
        id = add_entry(
            title=topic,
            content=content,
            category=cat_match,
            source=f"AI Autonomous Miner ({topic.split(':')[1].strip()})",
            tags=["autonomous", "hyper-depth", topic.split(':')[0].strip()]
        )
        
        if id:
            print(f"✅ Đã nạp thành công: {topic} [ID: {id}]")
        else:
            print(f"❌ Lỗi nạp dữ liệu cho: {topic}")
            
        time.sleep(2) # Prevent rate limits

    # 4. AUTONOMOUS CLEANUP (24/7 Cleanup Legion)
    print("🧹 Kích hoạt Quân đoàn Dọn dẹp tự động...")
    maintenance = MaintenanceManager()
    maintenance.run_cleanup_cycle()

if __name__ == "__main__":
    # For local testing, attempt to find a key
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("⚠️ Vui lòng đặt biến môi trường GEMINI_API_KEY để chạy script này.")
    else:
        print("🚀 Khởi chạy chu kỳ Khai thác Tự trị (Hyper-Depth)...")
        run_mining_cycle(key)
        print("✨ Hoàn tất chu kỳ.")
