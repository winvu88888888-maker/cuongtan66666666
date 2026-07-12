import sys
import os
import time
import random
import concurrent.futures
from datetime import datetime
import json

# Add paths for local import
current_dir = os.path.dirname(os.path.abspath(__file__)) # .../ai_modules
parent_dir = os.path.dirname(current_dir) # .../UPLOAD_TO_STREAMLIT

# Add parent dir to path to find gemini_helper.py
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    # Try relative imports first for when run as module
    from .shard_manager import add_entry
    from .mining_strategist import MiningStrategist
    from .gemini_expert_v172 import GeminiQMDGHelper
except (ImportError, ValueError):
    # Fallback to direct imports (GitHub Actions / CLI / Streamlit)
    try:
        from shard_manager import add_entry
        from mining_strategist import MiningStrategist
    except ImportError:
        # Final fallback: add current dir to path
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from shard_manager import add_entry
        from mining_strategist import MiningStrategist
    
    # GeminiQMDGHelper: try multiple sources
    try:
        from gemini_expert_v172 import GeminiQMDGHelper
    except ImportError:
        try:
            from gemini_helper import GeminiQMDGHelper
        except ImportError:
            # Minimal fallback so script doesn't crash
            class GeminiQMDGHelper:
                def __init__(self, api_key): self.api_key = api_key
                def _call_ai(self, prompt, **kwargs):
                    import google.generativeai as genai
                    genai.configure(api_key=self.api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    resp = model.generate_content(prompt)
                    return resp.text if resp else ""

try:
    import streamlit as st
except ImportError:
    # Stub for GitHub Actions where streamlit is not needed for mining
    class _StStub:
        def secrets(self): return {}
    st = _StStub()

CONFIG_PATH = os.path.join(os.path.dirname(current_dir), 'data_hub', 'factory_config.json')

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: pass
    return {"autonomous_247": False, "interval_minutes": 30}

def save_config(config):
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    except: pass

def _single_agent_task(agent_id, topic, api_key):
    """Công việc của một Agent đơn lẻ - UPGRADED với Web Search."""
    print(f"🤖 [Agent #{agent_id}] Đang tiếp nhận mục tiêu: {topic}...")
    
    try:
        strategist = MiningStrategist()
        ai_helper = GeminiQMDGHelper(api_key)
        
        # PHASE 1: Web Search để thu thập dữ liệu thô
        try:
            from web_searcher import get_web_searcher
            searcher = get_web_searcher()
            web_data = searcher.deep_research(topic, num_sources=3)
            print(f"✅ [Agent #{agent_id}] Đã thu thập dữ liệu web")
        except Exception as e:
            print(f"⚠️ [Agent #{agent_id}] Web search failed: {e}")
            web_data = ""
        
        # PHASE 2: AI Synthesis với dữ liệu web + Gemini Search
        mining_prompt = strategist.synthesize_mining_prompt(topic)
        # V13.0: Giới hạn web_data để tránh response quá lớn gây lỗi parsing
        if web_data:
            mining_prompt = f"{mining_prompt}\n\n**DỮ LIỆU THU THẬP TỪ WEB:**\n{str(web_data)[:2000]}"
        
        # V13.0: Thêm hướng dẫn format gọn cho AI
        mining_prompt += "\n\nTRẢ LỜI TRONG 800 CHỮ. KHÔNG viết quá dài."
        raw_content = ai_helper._call_ai(mining_prompt, use_hub=False, use_web_search=True)
        
        # V13.0: Cắt giới hạn response để tránh lỗi parsing JSON (Extra data error)
        if raw_content and len(raw_content) > 10000:
            raw_content = raw_content[:10000]
        
        # SMART FILTERING: Parse clean title and category from AI response
        clean_title = topic
        standard_category = "Kiến Thức"
        final_content = raw_content
        
        try:
            # Look for JSON block
            if "```json" in raw_content:
                parts = raw_content.split("```json")
                if len(parts) > 1:
                    json_str = parts[1].split("```")[0].strip()
                    meta = json.loads(json_str)
                    clean_title = meta.get("clean_title", topic)
                    standard_category = meta.get("standard_category", "Kiến Thức")
                    # Remove the JSON block from final content to keep it clean
                    final_content = raw_content.replace(f"```json{json_str}```", "").strip()
        except Exception as e:
            print(f"⚠️ [Agent #{agent_id}] Smart filtering parse failed: {e}")
        
        id = add_entry(
            title=clean_title,
            content=final_content,
            category=standard_category,
            source=f"Agent #{agent_id} (Quân Đoàn AI)",
            tags=["autonomous", "hyper-depth", f"agent-{agent_id}"]
        )
        
        if id:
            print(f"✅ [Agent #{agent_id}] KHAI THÁC THÀNH CÔNG: {topic}")
            return True
        else:
            print(f"❌ [Agent #{agent_id}] Thất bại khi lưu: {topic}")
            return False
            
    except Exception as e:
        print(f"⚠️ [Agent #{agent_id}] Gặp sự cố: {e}")
        return False

def run_mining_cycle(api_key, category=None):
    """Executes one full cycle of autonomous mining with THE 10 AI LEGION."""
    if not api_key:
        print("⚠️ Thiếu API Key.")
        return
        
    strategist = MiningStrategist()
    
    # Update stats
    config = load_config()
    config["last_run"] = time.strftime("%Y-%m-%d %H:%M:%S")
    config["total_cycles"] = config.get("total_cycles", 0) + 1
    save_config(config)

    print("\n" + "="*60)
    print(f"🚀 KÍCH HOẠT QUÂN ĐOÀN 10 AI - CHU KỲ #{config['total_cycles']}")
    print("="*60)

    # 1. Generate queue - V13.0: 4 AGENTS (tiết kiệm API, trước đó 10 agents quá nhiều)
    queue_size = 4
    initial_queue = strategist.generate_research_queue(category, count=queue_size)
    
    # DEDUPLICATION: Check hub_index to skip already researched topics
    try:
        from .shard_manager import search_index
    except (ImportError, ValueError):
        try:
            from shard_manager import search_index
        except ImportError:
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from shard_manager import search_index
    
    existing_entries = search_index()
    existing_titles = [e['title'].lower() for e in existing_entries]
    
    queue = []
    for t in initial_queue:
        t_lower = t.lower()
        # FUZZY DEDUP: Skip if exact match OR if core topic (first 30 chars) already exists
        is_dup = False
        for et in existing_titles:
            if t_lower == et or t_lower[:30] in et or et[:30] in t_lower:
                is_dup = True
                break
        if not is_dup and len(queue) < queue_size:
            queue.append(t)
    
    if not queue:
        print("✨ Tất cả chủ đề hiện tại đã được khai thác. Đang tạo chủ đề ngẫu nhiên mới...")
        queue = [f"{t} - Chuyên sâu Giai đoạn {random.randint(2, 5)}" for t in initial_queue[:10]]

    print(f"📡 Trung tâm chỉ huy đã phân phối {len(queue)} nhiệm vụ cho Quân đoàn AI...")
    
    # 2. Parallel Execution - V13.0: Giảm xuống 4 agents (tiết kiệm API quota)
    active_agents = min(len(queue), 4)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=active_agents) as executor:
        futures = []
        for i, topic in enumerate(queue):
            # Assign random Agent ID from 1-50
            agent_id = random.randint(1, 10) 
            futures.append(executor.submit(_single_agent_task, agent_id, topic, api_key))
            time.sleep(1) # Stagger start to be nice to API
            
        # Wait for all
        concurrent.futures.wait(futures)

    # Cleanup đã bị xóa vĩnh viễn theo yêu cầu người dùng.

    # 4. AUTO DEPLOY TO CLOUD (Git Push)
    # Tự động đồng bộ dữ liệu lên luồng Streamlit Cloud để web cập nhật
    print("\n" + "-"*40)
    print("☁️ Đang đồng bộ dữ liệu lên Đám Mây (Auto-Deploy)...")
    try:
        import subprocess
        # Gọi script sync_and_push.bat ở thư mục cha
        sync_script = os.path.join(parent_dir, "sync_and_push.bat")
        if os.path.exists(sync_script):
            subprocess.run([sync_script], shell=True, check=False)
            print("✅ Đã gửi lệnh đồng bộ thành công.")
        else:
            print(f"⚠️ Không tìm thấy script đồng bộ tại: {sync_script}")
    except Exception as e:
        print(f"⚠️ Lỗi đồng bộ đám mây: {e}")

def run_daemon():
    """Persistent 24/7 Loop"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║      🏭 NHÀ MÁY AI VÔ TẬN (INFINITE AI FACTORY)      ║
    ║           Chế độ: 24/7 Autonomous Daemon             ║
    ║      Tình trạng: 🟢 ĐANG CHẠY (Background Mode)      ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    error_count = 0
    
    while True:
        # Reload config to check for stop signal (BUT default to TRUE if running from CLI daemon)
        config = load_config()
        
        # Logic: If config says False, we pause but don't exit script completely (wait for enable)
        # unless user kills script.
        
        api_key = config.get("api_key") or os.getenv("GEMINI_API_KEY")
        
        # 1. Truy tìm Key trong secrets.toml của Streamlit
        if not api_key:
            try:
                secrets_path = os.path.join(os.path.dirname(current_dir), ".streamlit", "secrets.toml")
                if os.path.exists(secrets_path):
                    with open(secrets_path, "r", encoding="utf-8") as f:
                        for line in f:
                            if "GEMINI_API_KEY" in line or "gemini_key" in line:
                                parts = line.split("=")
                                if len(parts) >= 2:
                                    found_key = parts[1].strip().strip('"').strip("'")
                                    if found_key:
                                        api_key = found_key
                                        print(f"✅ Đã tìm thấy API Key từ secrets.toml")
                                        # Save to factory config for future
                                        config["api_key"] = api_key
                                        save_config(config)
                                        break
            except: pass

        # 2. Truy tìm Key trong custom_data.json (Do app.py lưu)
        if not api_key:
            try:
                custom_data_path = os.path.join(os.path.dirname(current_dir), "custom_data.json")
                if os.path.exists(custom_data_path):
                    with open(custom_data_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        found_key = data.get("GEMINI_API_KEY")
                        if found_key:
                            api_key = found_key
                            print(f"✅ Đã tìm thấy API Key từ custom_data.json")
                            # AUTO-SYNC: Lưu vào factory config để dùng cho các lần sau
                            config["api_key"] = api_key
                            save_config(config)
                            print(f"🔄 Đã đồng bộ API Key vào factory_config.json")
            except: pass

        # 3. Nếu vẫn chưa có, hỏi người dùng NHẬP TRỰC TIẾP
        if not api_key:
            print("\n❌ CHƯA TÌM THẤY API KEY.")
            print("👉 Vui lòng nhập Gemini API Key của bạn vào bên dưới để cấu hình một lần duy nhất.")
            print("(Key sẽ được lưu vào factory_config.json và custom_data.json để tự động chạy các lần sau)")
            try:
                user_input_key = input("🔑 Nhập API Key: ").strip()
                if user_input_key and len(user_input_key) > 10:
                    api_key = user_input_key
                    config["api_key"] = api_key
                    save_config(config)
                    
                    # CỰC KỲ QUAN TRỌNG: Lưu đồng thời vào custom_data.json cho app.py thấy
                    try:
                        custom_data_path = os.path.join(os.path.dirname(current_dir), "custom_data.json")
                        c_data = {}
                        if os.path.exists(custom_data_path):
                            with open(custom_data_path, 'r', encoding='utf-8') as f:
                                c_data = json.load(f)
                        c_data["GEMINI_API_KEY"] = api_key
                        with open(custom_data_path, 'w', encoding='utf-8') as f:
                            json.dump(c_data, f, ensure_ascii=False, indent=4)
                        print(f"✅ Đã lưu cấu hình và đồng bộ sang custom_data.json")
                    except: pass
                    
                    print("✅ Khởi động thành công!")
                else:
                    print("⚠️ Key không hợp lệ. Đang thử lại sau 60s...")
                    time.sleep(60)
                    continue
            except Exception:
                # Trường hợp không input được (ví dụ chạy ngầm hoàn toàn không tương tác)
                time.sleep(60)
                continue
            
        # Run Cycle
        try:
            run_mining_cycle(api_key)
            error_count = 0 # Reset error count on success
        except Exception as e:
            error_count += 1
            print(f"🔥 Lỗi hệ thống: {e}")
            if error_count > 10:
                print("⚠️ Quá nhiều lỗi liên tiếp. Tạm dừng 10 phút...")
                time.sleep(600)
                error_count = 0
            
        # Sleep
        interval = config.get("interval_minutes", 15) # Default faster (15 mins)
        if interval < 1: interval = 1
        
        next_run = time.time() + (interval * 60)
        print(f"\n⏳ Quân đoàn AI nghỉ ngơi {interval} phút...")
        print(f"⏰ Chu kỳ tiếp theo: {datetime.fromtimestamp(next_run).strftime('%H:%M:%S')}")
        
        # Countdown visual (optional)
        time.sleep(interval * 60)

if __name__ == "__main__":
    # Check if running in GitHub Actions
    is_github_action = os.getenv("GITHUB_ACTIONS") == "true"
    
    if "--daemon" in sys.argv and not is_github_action:
        # Force enable in config if running explicitly
        c = load_config()
        c["autonomous_247"] = True
        save_config(c)
        run_daemon()
    else:
        # One-off run (Local or GitHub Action)
        print("🚀 Chạy chế độ One-Off (Khai thác 1 lần rồi nghỉ)...")
        
        # Priority: Env Var (GitHub Secrets) -> Config -> Custom Data
        key = os.environ.get("GEMINI_API_KEY")
        
        if not key:
            # Try load from config
            c = load_config()
            key = c.get("api_key")
            
        if not key:
             # Try custom_data.json
             try:
                custom_data_path = os.path.join(os.path.dirname(current_dir), "custom_data.json")
                if os.path.exists(custom_data_path):
                    with open(custom_data_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        key = data.get("GEMINI_API_KEY")
             except: pass

        if key:
            run_mining_cycle(key)
        else:
            print("❌ Không tìm thấy Key. (Nếu chạy trên GitHub, hãy set Secret GEMINI_API_KEY)")
            # Trên GitHub Actions, không error exit để tránh báo đỏ cả workflow nếu chỉ thiếu key
            if is_github_action:
                print("⚠️ Bỏ qua chu kỳ này do thiếu Key.")
            else:
                print("❌ Startup bypassed: Missing Key.")
