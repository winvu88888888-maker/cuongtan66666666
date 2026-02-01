"""
Enhanced Gemini Helper with Context Awareness - V1.7.3
Gemini sẽ tự động biết ngữ cảnh: cung nào, chủ đề gì, đang xem phần nào
"""

import google.generativeai as genai
import os
import requests
import json
import time
import hashlib

# --- DATA CONSTANTS ---
CUNG_NGU_HANH = {
    1: "Thủy",
    2: "Thổ",
    3: "Mộc",
    4: "Mộc",
    5: "Thổ",
    6: "Kim",
    7: "Kim",
    8: "Thổ",
    9: "Hỏa"
}

CUNG_TEN = {
    1: "Khảm (Thủy)",
    2: "Khôn (Thổ)",
    3: "Chấn (Mộc)",
    4: "Tốn (Mộc)",
    5: "Trung Cung (Thổ)",
    6: "Càn (Kim)",
    7: "Đoài (Kim)",
    8: "Cấn (Thổ)",
    9: "Ly (Hỏa)"
}

QUAI_NAMES = {1: "Khảm", 2: "Khôn", 3: "Chấn", 4: "Tốn", 6: "Càn", 7: "Đoài", 8: "Cấn", 9: "Ly"}
QUAI_ELEMENTS = {1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"}


class GeminiQMDGHelperV173:
    """
    Helper class for Gemini AI with QMDG specific knowledge and grounding - V1.7.3
    """
    _response_cache = {}
    _cache_max_size = 100
    
    def __init__(self, api_key):
        """Initialize Gemini with API key and super intelligence features"""
        self.api_key = api_key
        self.version = "V1.7.5"
        genai.configure(api_key=api_key)
        self._failed_models = set() # Track exhausted models
        self.max_retries = 3
        self.base_delay = 2
        self.hub_searcher = None
        self.n8n_webhook_url = None
        
        # Initialize Hub Searcher
        try:
            from ai_modules.hub_searcher import HubSearcher
            self.hub_searcher = HubSearcher()
        except:
            print("⚠️ Hub Searcher could not be initialized.")

        self.model_priority = [
            "gemini-flash-latest",
            "gemini-pro-latest",
            "gemini-2.0-flash",
            "gemini-exp-1206",
        ]
        self.model = self._get_best_model()

        # Context Memory
        self.current_context = {
            "chart_data": None,
            "topic": None,
            "last_action": None,
            "palace": None
        }

    def _get_cache_key(self, prompt):
        """Generate cache key from prompt"""
        return hashlib.md5(prompt.encode('utf-8')).hexdigest()
        
    def _get_cached_response(self, prompt):
        """Get cached response if exists and not expired"""
        key = self._get_cache_key(prompt)
        if key in self._response_cache:
            entry = self._response_cache[key]
            # Expire after 10 minutes
            if time.time() - entry['time'] < 600:
                print("⚡ Using cached AI response")
                return entry['response']
        return None

    def _cache_response(self, prompt, response):
        """Cache a response"""
        key = self._get_cache_key(prompt)
        # Prune if too big
        if len(self._response_cache) >= self._cache_max_size:
            # Remove oldest
            oldest = min(self._response_cache.items(), key=lambda x: x[1]['time'])
            del self._response_cache[oldest[0]]
            
        self._response_cache[key] = {
            'response': response,
            'time': time.time()
        }

    def set_n8n_url(self, url):
        self.n8n_webhook_url = url

    def _get_best_model(self):
        """Find the best available model for the current API key"""
        # Try finding a working model from priority list
        for model_name in self.model_priority:
            if model_name in self._failed_models:
                continue
            try:
                m = genai.GenerativeModel(model_name)
                # Quick test to see if we have access / quota
                # We skip the network test to speed up startup, relying on lazy error handling during main call
                # m.generate_content("Ping", request_options={"timeout": 5}) 
                print(f"✅ Selected Model: {model_name}")
                return m
            except Exception as e:
                print(f"⚠️ Model {model_name} failed check: {e}")
                
        # Fallback to flash if all else fails
        return genai.GenerativeModel("gemini-1.5-flash")

    def test_connection(self):
        """Quickly test if the API key and model are working"""
        try:
            response = self.model.generate_content("Hello", request_options={"timeout": 10})
            return True, f"Kết nối thành công tới model {self.model.model_name}!"
        except Exception as e:
            try:
                # DEBUG: List available models
                available = []
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        available.append(m.name)
                
                if not available:
                    return False, f"Lỗi: API Key này không thấy model nào cả. (Danh sách rỗng). Vui lòng tạo Key mới."
                
                return False, f"Lỗi kết nối: {str(e)}. Model khả dụng: {', '.join(available)}"
            except Exception as e2:
                return False, f"Lỗi kết nối: {str(e)}. Không thể liệt kê model: {str(e2)}"

    def _fetch_relevant_hub_data(self, query):
        """Fetch the most relevant context from the Sharded Hub."""
        if not self.hub_searcher: return ""
        try:
            results = self.hub_searcher.search(query, max_results=3)
            if not results: return ""
            
            context_str = "\n\n**KIẾN THỨC TỪ HUB:**\n"
            for res in results:
                context_str += f"- [{res['category']}] {res['title']}: {res['content_snippet'][:200]}...\n"
            return context_str
        except:
            return ""

    def safe_get_text(self, response):
        """Safely extract text from Gemini response, handling safety blocks"""
        try:
            return response.text
        except ValueError:
            # Handle blocked content
            if response.prompt_feedback:
                if response.prompt_feedback.block_reason:
                    return "⚠️ AI từ chối trả lời vì lý do an toàn (Safety Filter)."
            return "⚠️ Không có phản hồi văn bản (Lỗi không xác định)."

    def _call_ai(self, prompt, use_hub=True, use_web_search=False):
        """Call AI with auto-switch fallback, caching, and improved retry logic."""
        
        # Check cache
        cached = self._get_cached_response(prompt)
        if cached: return cached

        # Inject Hub Knowledge
        if use_hub:
            hub_context = self._fetch_relevant_hub_data(prompt[-100:]) # Search based on end of prompt
            if hub_context:
                prompt = hub_context + "\n" + prompt

        # --- N8N HANDOFF (DISABLED FOR DEBUGGING) ---
        # if self.n8n_webhook_url:
        #     try:
        #         print(f"🚀 Forwarding to n8n: {self.n8n_webhook_url}")
        #         payload = {"prompt": prompt}
        #         resp = requests.post(self.n8n_webhook_url, json=payload, timeout=30)
        #         if resp.status_code == 200:
        #             result = resp.json().get('output', "n8n processed request but returned no output.")
        #             self._cache_response(prompt, result)
        #             return result
        #     except Exception as e:
        #         print(f"⚠️ n8n Error: {e}. Falling back to direct Gemini.")

        # --- DIRECT GEMINI CALL ---
        last_error = ""
        
        for attempt in range(self.max_retries):
            try:
                # Add Web Search capability check (Not native in standard API yet unless using Vertex/special tools)
                # But we can simulate context injection via web_searcher tool if passed in higher level.
                # Here we rely on standard generate_content.
                
                response = self.model.generate_content(prompt)
                
                # Success
                text = self.safe_get_text(response)
                
                # Prepend debug tag
                text = "**🔮 [PYTHON V1.7.5 DIRECT]**\n\n" + text
                
                self._cache_response(prompt, text)
                return text

            except Exception as e:
                error_msg = str(e)
                last_error = error_msg
                print(f"⚠️ AI Call Error (Attempt {attempt+1}): {error_msg}")
                
                # Handle Quota -> Switch Model
                if "429" in error_msg or "quota" in error_msg.lower():
                    self._failed_models.add(self.model.model_name)
                    print(f"⚠️ Model {self.model.model_name} exhausted. Switching...")
                    self.model = self._get_best_model()
                    time.sleep(2)
                    continue
                
                time.sleep(2) # Retry delay
                continue
                    
        return f"❌ Lỗi AI sau {self.max_retries} lần thử: {last_error}"

    def update_context(self, **kwargs):
        """Update current context"""
        self.current_context.update(kwargs)
    
    def get_system_knowledge(self):
        """Returns string representation of key system rules for AI context"""
        return """
**QUY TẮC LUẬN GIẢI CHUYÊN SÂU (V1.7.3):**
1. **Nguyên lý Sinh Khắc:** Thủy(1)->Mộc(3,4)->Hỏa(9)->Thổ(2,8,5)->Kim(6,7)->Thủy(1).
2. **Dụng Thần:** Yếu tố đại diện cho sự việc.
3. **Bản Mệnh:** Đại diện cho người hỏi (Can Ngày).
4. **Kết Luận:** Dựa vào sinh khắc giữa Cung Bản Mệnh và Cung Dụng Thần.
"""

    def get_context_prompt(self):
        """Build context prompt from current state"""
        context_parts = []
        context_parts.append(self.get_system_knowledge())
        
        if self.current_context.get('topic'):
            context_parts.append(f"**Chủ đề hiện tại:** {self.current_context['topic']}")
        
        if context_parts:
            return "\n".join(["**NGỮ CẢNH HỆ THỐNG:**"] + context_parts) + "\n\n"
        return ""
    
    def classify_topic_intent(self, topic):
        """Classify topic"""
        topic_lower = topic.lower()
        if any(kw in topic_lower for kw in ['đánh', 'cá cược', 'xổ số', 'cờ bạc']): return 'GAMBLING'
        if any(kw in topic_lower for kw in ['sức khỏe', 'bệnh', 'chữa']): return 'HEALTH'
        if any(kw in topic_lower for kw in ['kinh doanh', 'đầu tư', 'lợi nhuận']): return 'BUSINESS'
        if any(kw in topic_lower for kw in ['tình', 'yêu', 'hôn nhân']): return 'RELATIONSHIP'
        return 'GENERAL'
    
    def search_knowledge_hub(self, query, category=None, max_results=3):
        """Search knowledge hub"""
        if not self.hub_searcher: return []
        try: return self.hub_searcher.search(query, category=category, max_results=max_results)
        except: return []

    # --- MAIN Q&A METHOD (STRICTLY FIXED FOR V1.7.3) ---
    def answer_question(self, question, chart_data=None, topic=None):
        """
        Answer with FULL CONTEXT AWARENESS & NO LISTING
        """
        if chart_data is None: chart_data = self.current_context.get('chart_data')
        if topic is None: topic = self.current_context.get('topic', 'Chung')
        
        self.update_context(topic=topic, chart_data=chart_data, last_action=f"[V1.7.3] {question[:50]}...")
        
        context = self.get_context_prompt()
        chart_context = ""
        deep_knowledge = ""
        
        if chart_data:
            # 1. Identify Key Actors
            day_stem = (chart_data.get('can_ngay', '') or '').split(' ')[0]
            hour_stem = (chart_data.get('can_gio', '') or '').split(' ')[0]
            
            day_palace = None
            hour_palace = None
            
            for i in range(1, 10):
                stem_heaven = chart_data.get('can_thien_ban', {}).get(i)
                if stem_heaven == day_stem: day_palace = i
                if stem_heaven == hour_stem: hour_palace = i
            
            # 2. Build Focused Description
            search_queries = []
            context_items = []
            
            def get_palace_desc(p_idx, label):
                if not p_idx: return ""
                sao = chart_data.get('thien_ban', {}).get(p_idx, 'N/A')
                mon = chart_data.get('nhan_ban', {}).get(p_idx, 'N/A')
                than = chart_data.get('than_ban', {}).get(p_idx, 'N/A')
                can_thien = chart_data.get('can_thien_ban', {}).get(p_idx, 'N/A')
                can_dia = chart_data.get('dia_can', {}).get(p_idx, 'N/A')
                
                search_queries.append(f"Ý nghĩa sao {sao} cửa {mon} trong kỳ môn độn giáp")
                return (f"- **{label} (Cung {p_idx})**: "
                        f"Gặp sao **{sao}**, cửa **{mon}**, thần **{than}**. "
                        f"Thiên bàn **{can_thien}** trên địa bàn **{can_dia}**.")

            if day_palace:
                context_items.append(get_palace_desc(day_palace, f"BẢN MỆNH NGƯỜI HỎI (Can Ngày {day_stem})"))
            if hour_palace and hour_palace != day_palace:
                context_items.append(get_palace_desc(hour_palace, f"VẤN ĐỀ CẦN HỎI (Can Giờ {hour_stem})"))

            # 3. Web Search
            if search_queries:
                try:
                    from ai_modules.web_searcher import get_web_searcher
                    searcher = get_web_searcher()
                    dk_results = []
                    for q in search_queries[:2]:
                        res = searcher.search_google(q, num_results=2)
                        for r in res: dk_results.append(f"- {r.get('title')}: {r.get('snippet')[:100]}")
                    if dk_results:
                        deep_knowledge = "\n**KIẾN THỨC BỔ TRỢ (GOOGLE):**\n" + "\n".join(dk_results)
                except: pass
                
            chart_context = "\n**DỮ LIỆU CỐT LÕI (CHỈ XÉT BẢN MỆNH & SỰ VIỆC):**\n" + "\n".join(context_items)

        prompt = f"""{context}Bạn là ĐẠI PHÁP SƯ KỲ MÔN (V1.7.3) - Người nhìn thấu thiên cơ.

**BỐI CẢNH:**
- Chủ đề: "{topic}"
{chart_context}
{deep_knowledge}

**CÂU HỎI:** "{question}"

**NHIỆM VỤ:**
1. **Luận Giải**: Dựa vào Sao/Môn ở Cung Bản Mệnh và Cung Sự Việc trên, giải thích tại sao tốt/xấu?
2. **Kết Luận**: Đi thẳng vào kết quả (Thành hay Bại, Cát hay Hung).
3. **Lời Khuyên**: Một hành động cụ thể để cải mệnh.

**TUYỆT ĐỐI KHÔNG LIỆT KÊ CÁC CUNG KHÁC.** Chỉ tập trung vào Bản Mệnh và Sự Việc.
Trả lời sắc sảo, ngắn gọn, phong cách huyền bí nhưng thực tế.
"""
        return self._call_ai(prompt, use_hub=True, use_web_search=True)

    def explain_element(self, element_type, element_name):
        """Explain element"""
        prompt = f"Giải thích ngắn gọn 3 dòng về ý nghĩa của {element_type} {element_name} trong Kỳ Môn Độn Giáp. Tập trung vào Cát/Hung."
        return self._call_ai(prompt)

    # ... Include other analysis methods if needed, simplified for brevity but functional ...
    # Integrating core expert logic for full analysis view
    def comprehensive_analysis(self, chart_data, topic, **kwargs):
        return self.answer_question(f"Hãy phân tích tổng quan lá số này cho chủ đề {topic}.", chart_data, topic)

    def analyze_palace(self, palace_data, topic):
        self.answer_question(f"Phân tích chi tiết cung {palace_data.get('num')} cho việc {topic}.", {'can_ngay': 'X', 'can_thien_ban': {palace_data['num']: 'X'}}, topic) # Dummy data to force palace focus logic if needed, or just use prompt
        # Actually better to use specific prompt
        return self._call_ai(f"Phân tích Cung {palace_data} cho chủ đề {topic}. Đưa ra dự đoán định lượng % thành công.")

    def analyze_mai_hoa(self, mai_hoa_res, topic="Chung"):
        prompt = f"Luận giải quẻ Mai Hoa: {mai_hoa_res}. Chủ đề: {topic}. Kết luận Cát/Hung."
        return self._call_ai(prompt)

    def analyze_luc_hao(self, luc_hao_res, topic="Chung"):
        prompt = f"Luận giải Lục Hào: {luc_hao_res['ban']['name']} biến {luc_hao_res['bien']['name']}. Chủ đề: {topic}."
        return self._call_ai(prompt)

# Compatibility Alias
GeminiQMDGHelper = GeminiQMDGHelperV173
