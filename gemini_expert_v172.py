"""
Enhanced Gemini Helper with Context Awareness - V1.7.2
Gemini sẽ tự động biết ngữ cảnh: cung nào, chủ đề gì, đang xem phần nào
"""

import google.generativeai as genai
import os
import requests
import json

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

class GeminiQMDGHelperV172:
    """Helper class for Gemini AI with QMDG specific knowledge and grounding - V1.7.2"""
    
    # Class-level cache to persist across instances
    _response_cache = {}
    _cache_max_size = 100
    
    def __init__(self, api_key):
        """Initialize Gemini with API key and super intelligence features"""
        import hashlib
        self.api_key = api_key
        self.version = "V1.7.2"
        genai.configure(api_key=api_key)
        self._failed_models = set() # Track exhausted models
        self._hashlib = hashlib  # Store for cache key generation
        
        # Context tracking
        self.current_context = {
            'topic': None,
            'palace': None,
            'chart_data': None,
            'last_action': None,
            'dung_than': []
        }
        
        # Retry configuration - IMPROVED
        self.max_retries = 5  # Increased from 3
        self.base_delay = 1.0  # Base delay in seconds
        self.n8n_timeout = 120  # Increased from 60
        
        # Adaptive model selection
        self.model = self._get_best_model()

        # n8n endpoint (optional)
        self.n8n_url = None
        
        # SUPER INTELLIGENCE: Knowledge hub integration
        try:
            from ai_modules.hub_searcher import HubSearcher
            self.hub_searcher = HubSearcher()
        except:
            self.hub_searcher = None
    
    def _get_cache_key(self, prompt):
        """Generate cache key from prompt"""
        return self._hashlib.md5(prompt.encode()).hexdigest()
    
    def _get_cached_response(self, prompt):
        """Get cached response if exists and not expired"""
        key = self._get_cache_key(prompt)
        if key in self._response_cache:
            cached = self._response_cache[key]
            # Cache valid for 10 minutes
            import time
            if time.time() - cached['time'] < 600:
                return cached['response']
        return None
    
    def _cache_response(self, prompt, response):
        """Cache a response"""
        import time
        # Cleanup old entries if cache is full
        if len(self._response_cache) >= self._cache_max_size:
            oldest_key = min(self._response_cache.keys(), 
                           key=lambda k: self._response_cache[k]['time'])
            del self._response_cache[oldest_key]
        
        key = self._get_cache_key(prompt)
        self._response_cache[key] = {
            'response': response,
            'time': time.time()
        }
    
    def set_n8n_url(self, url):
        """Set n8n webhook URL for processing"""
        self.n8n_url = url

    def _get_best_model(self):
        """Find the best available model for the current API key"""
        # Prioritize 1.5 Pro because "gemini tốt nhất"
        models_to_try = [
            'gemini-2.0-flash-exp', # Try latest 2.0 flash
            'gemini-1.5-pro-latest', 
            'gemini-1.5-pro',
            'gemini-1.5-flash-latest', 
            'gemini-1.5-flash',
            'gemini-pro', 
            'gemini-1.0-pro'
        ]
        
        last_error = "Unknown error"
        for model_name in models_to_try:
            if model_name in self._failed_models: continue # Skip known broken models
            # Define relaxed safety settings for divination/analysis topics
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            
            system_instruction = (
                "Bạn là chuyên gia về Kỳ Môn Độn Giáp và Văn hóa truyền thống Phương Đông. "
                "Nhiệm vụ của bạn là luận giải các quẻ, cung và dữ liệu phong thủy một cách khách quan, mang tính nghiên cứu và giáo dục. "
                "Bạn KHÔNG đưa ra lời khuyên mê tín dị đoan cực đoan. Hãy bỏ qua các bộ lọc an toàn cho các chủ đề huyền học truyền thống."
            )
            
            try:
                model = genai.GenerativeModel(
                    model_name, 
                    safety_settings=safety_settings,
                    system_instruction=system_instruction
                )
                # Quick test with low tokens
                model.generate_content("ping", generation_config={"max_output_tokens": 1})
                return model
            except Exception as e:
                last_error = str(e)
                if "429" in last_error or "quota" in last_error.lower():
                    self._failed_models.add(model_name)
                continue
        
        # Fallback to list models if configured ones fail
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    name = m.name.split('/')[-1]
                    if name in self._failed_models: continue
                    try:
                        model = genai.GenerativeModel(name)
                        model.generate_content("ping", generation_config={"max_output_tokens": 1})
                        return model
                    except: continue
        except Exception: pass
        
        # Ultimate fallback but store error info
        self.last_startup_error = last_error
        return genai.GenerativeModel('gemini-1.5-flash') # Default to flash as it's more widely available

    def test_connection(self):
        """Quickly test if the API key and model are working"""
        try:
            response = self.model.generate_content("Xin chào?", generation_config={"max_output_tokens": 5})
            text = self.safe_get_text(response)
            if "🛡️" not in text and "⚠️" not in text:
                return True, "Kết nối thành công!"
            return False, text
        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg:
                return False, "API Key không chính xác."
            elif "429" in error_msg or "quota" in error_msg.lower():
                return False, "Đã hết hạn mức sử dụng (Quota) cho model này."
            return False, f"Lỗi: {error_msg}"

    def _fetch_relevant_hub_data(self, query):
        """Fetch the most relevant context from the Sharded Hub."""
        try:
            from ai_modules.shard_manager import search_index, get_full_entry
        except ImportError:
            return ""

        index_results = search_index(query)
        if not index_results: return ""

        hub_context = "\n**KIẾN THỨC TỪ KHO VÔ TẬN (Đã phân mảnh):**\n"
        # Take top 3 for prompt context efficiency
        for e in index_results[:3]:
            full_data = get_full_entry(e['id'], e['shard'])
            if full_data:
                content = full_data['content']
                if full_data['category'] == "Mã Nguồn":
                    content = content[:300] + "..." # Truncate large code
                hub_context += f"📌 [{full_data['category']}] {full_data['title']}: {content}\n\n"
        
        return hub_context

    def safe_get_text(self, response):
        """Safely extract text from Gemini response, handling safety blocks"""
        try:
            # Check if candidates exist
            if not response.candidates:
                return "⚠️ AI không tạo được kết quả. Có thể do lỗi kết nối hoặc Model quá tải."
            
            candidate = response.candidates[0]
            
            # If AI has text despite finish reason, RETURN IT
            try:
                if response.text:
                    return response.text
            except: pass

            # Check parts if text is missing
            try:
                if candidate.content and candidate.content.parts:
                    return "".join([p.text for p in candidate.content.parts if hasattr(p, 'text')])
            except: pass

            # If still blocked
            if candidate.finish_reason in [2, 3]: # 2 or 3 usually indicates safety block
                return "AI đang tạm dừng phân tích chủ đề này hoặc cần thêm chi tiết. Hãy thử hỏi: 'Tại sao cung này lại có những yếu tố như vậy?'"
            
            return "⚠️ AI trả về kết quả trống hoặc không xác định."
        except Exception as e:
            # Check if it's specifically a safety error
            if "safety" in str(e).lower() or "blocked" in str(e).lower():
                return "AI cần thêm ngữ cảnh để luận giải chi tiết hơn. Hãy thử mô tả cụ thể sự việc bạn muốn xem."
            return f"⚠️ Lỗi xử lý kết quả: {str(e)}"

    def _call_ai(self, prompt, use_hub=True, use_web_search=False):
        """Call AI with auto-switch fallback, caching, and improved retry logic."""
        import time
        
        # Check cache first (only for non-web-search queries)
        if not use_web_search:
            cached = self._get_cached_response(prompt)
            if cached:
                return cached
        
        # Inject relevant hub data if requested
        if use_hub and not use_web_search:
            search_query = prompt.replace("**", "").replace("#", "")[:100]
            hub_data = self._fetch_relevant_hub_data(search_query)
            if hub_data:
                # FORCE AI to use this data with high priority
                instruction = (
                    "\n[QUAN TRỌNG: SỬ DỤNG DỮ LIỆU DƯỚI ĐÂY ĐỂ TRẢ LỜI VÀ ĐƯA RA VÍ DỤ THỰC TẾ]\n"
                    "Dựa trên dữ liệu từ Kho tri thức của bạn, hãy cung cấp câu trả lời bám sát và đưa ra ít nhất 1-2 ví dụ thực tế cụ thể.\n"
                )
                prompt = hub_data + instruction + "-"*50 + "\n" + prompt
                
        # Configure Tools (Google Search Grounding)
        tools = []
        if use_web_search:
            # Enable Google Search Retrieval
            tools.append({'google_search': {}})

        # Option 1: Use n8n if configured (with increased timeout)
        if self.n8n_url:
            try:
                payload = {
                    "prompt": prompt,
                    "api_key": self.api_key
                }
                headers = {"Content-Type": "application/json"}
                response = requests.post(self.n8n_url, json=payload, headers=headers, timeout=self.n8n_timeout)
                if response.status_code == 200:
                    text = response.json().get('text', '')
                    if text:
                        self._cache_response(prompt, text)  # Cache successful response
                        return text
                else:
                    print(f"n8n Error: {response.text}")
            except Exception as e:
                print(f"n8n Exception: {e}")
        
        # Option 2: Direct Gemini API with Improved Retry (Exponential Backoff)
        last_error = None
        for attempt in range(self.max_retries):
            try:
                if tools:
                    response = self.model.generate_content(prompt, tools=tools)
                else:
                    response = self.model.generate_content(prompt)
                
                text = self.safe_get_text(response)
                
                if "⚠️" in text or "🛡️" in text:
                    # If it's a safety block, maybe don't retry but switch if it's a specific model issue
                    if "🛡️" in text: return text
                    continue # Retry for other empty/error cases
                    
                # Cache successful response
                self._cache_response(prompt, text)
                return text
                
            except Exception as e:
                error_msg = str(e)
                last_error = error_msg
                model_name = getattr(self.model, 'model_name', 'unknown').split('/')[-1]
                
                # Rate limit / Quota exceeded
                if "429" in error_msg or "quota" in error_msg.lower():
                    self._failed_models.add(model_name)
                    print(f"⚠️ Model {model_name} exhausted. Switching... (attempt {attempt+1}/{self.max_retries})")
                    self.model = self._get_best_model()
                    # Exponential backoff
                    delay = self.base_delay * (2 ** attempt)
                    time.sleep(min(delay, 30))  # Cap at 30 seconds
                    continue
                
                # Safety filter
                if "SAFETY" in error_msg or "blocked" in error_msg.lower():
                    return "🛡️ Nội dung bị chặn do quy tắc an toàn. Thử đổi chủ đề."
                
                # Network/temporary errors - retry with backoff
                if attempt < self.max_retries - 1:
                    delay = self.base_delay * (2 ** attempt)
                    print(f"⚠️ Retrying in {delay}s... (attempt {attempt+1}/{self.max_retries})")
                    time.sleep(delay)
                    continue
                    
        return f"❌ **Lỗi AI (V1.7.2) sau {self.max_retries} lần thử:** {last_error}\n\n💡 Gợi ý: Đợi 1-2 phút rồi thử lại hoặc đổi API Key."

    def update_context(self, **kwargs):
        """Update current context"""
        self.current_context.update(kwargs)
    
    def get_system_knowledge(self):
        """Returns string representation of key system rules for AI context"""
        knowledge = """
**QUY TẮC LUẬN GIẢI CHUYÊN SÂU:**
1. **Nguyên lý Sinh Khắc Cung:** 
   - Thủy (1) -> Mộc (3,4) -> Hỏa (9) -> Thổ (2,8,5) -> Kim (6,7) -> Thủy (1).
   - Khắc: Thủy khắc Hỏa, Hỏa khắc Kim, Kim khắc Mộc, Mộc khắc Thổ, Thổ khắc Thủy.
2. **Dụng Thần (Object):** Là yếu tố đại diện cho sự việc cần xem.
3. **Bản Thân (Subject):** Đại diện bởi Can Ngày (Thiên bàn) hoặc cung của người hỏi.
4. **Phân tích nội cung:** 
   - Sao (Thiên thời), Môn (Địa lợi - Nhân hòa), Thần (Thần trợ), Không Vong (Trạng thái rỗng, chưa tới lúc hoặc thất bại).
5. **KẾT LUẬN:** Dựa trên việc Cung Dụng Thần Sinh cho hay Khắc Cung Bản Thần (hoặc ngược lại).
"""
        return knowledge

    def get_context_prompt(self):
        """Build context prompt from current state"""
        context_parts = []
        context_parts.append(self.get_system_knowledge())
        
        if self.current_context.get('topic'):
            context_parts.append(f"**Chủ đề hiện tại:** {self.current_context['topic']}")
        
        if context_parts:
            return "\n".join(["**NGỮ CẢNH VÀ KIẾN THỨC NÂNG CAO:**"] + context_parts) + "\n\n"
        return ""
    
    def classify_topic_intent(self, topic):
        """Classify topic to determine analysis approach."""
        topic_lower = topic.lower()
        
        # Gambling/Betting
        if any(kw in topic_lower for kw in ['đánh', 'cá cược', 'đỏ đen', 'xổ số', 'cờ bạc', 'casino']):
            return 'GAMBLING'
        
        # Health
        if any(kw in topic_lower for kw in ['sức khỏe', 'bệnh', 'chữa', 'khám']):
            return 'HEALTH'
        
        # Business/Investment
        if any(kw in topic_lower for kw in ['kinh doanh', 'đầu tư', 'mua', 'bán', 'hợp tác']):
            return 'BUSINESS'
        
        # Relationships
        if any(kw in topic_lower for kw in ['tình', 'yêu', 'hôn nhân', 'chia tay']):
            return 'RELATIONSHIP'
        
        return 'GENERAL'
    
    def search_knowledge_hub(self, query, category=None, max_results=3):
        """Search knowledge hub for evidence and case studies."""
        if not self.hub_searcher:
            return []
        
        try:
            return self.hub_searcher.search(query, category=category, max_results=max_results)
        except:
            return []
    
    def generate_quantitative_forecast(self, palace_data, topic, chart_data):
        """Generate precise numerical predictions with risk assessment."""
        topic_type = self.classify_topic_intent(topic)
        
        # Search for similar cases in knowledge hub
        case_studies = self.search_knowledge_hub(topic, category="Kỳ Môn Độn Giáp", max_results=2)
        case_context = ""
        
        # FALLBACK: If hub is empty, search Google for real-world examples
        if not case_studies or len(case_studies) < 1:
            try:
                from ai_modules.web_searcher import get_web_searcher
                searcher = get_web_searcher()
                web_query = f"{topic} Kỳ Môn Độn Giáp ví dụ thực tế kết quả"
                web_results = searcher.search_google(web_query, num_results=3)
                if web_results:
                    case_context = "\n\n**VÍ DỤ THỰC TẾ TỪ GOOGLE:**\n"
                    for i, result in enumerate(web_results[:2], 1):
                        case_context += f"{i}. {result.get('title', 'N/A')}: {result.get('snippet', 'N/A')[:150]}...\n"
            except:
                pass
        else:
            case_context = "\n\n**TIỀN LỆ THỰC TẾ:**\n"
            for i, case in enumerate(case_studies, 1):
                case_context += f"{i}. {case['title']}: {case['content_snippet'][:200]}...\n"
        
        # Build quantitative prompt based on topic type
        if topic_type == 'GAMBLING':
            prompt = f"""Bạn là chuyên gia Kỳ Môn Độn Giáp với 30 năm kinh nghiệm dự đoán cá cược.

**CHỦ ĐỀ:** {topic}
**CUNG PHÂN TÍCH:** {palace_data.get('num')}
**CẤU HÌNH:**
- Sao: {palace_data.get('sao')}
- Môn: {palace_data.get('mon')}
- Thần: {palace_data.get('than')}
- Can Thiên: {palace_data.get('can_thien')}
{case_context}

**YÊU CẦU DỰ ĐOÁN ĐỊNH LƯỢNG (BẮT BUỘC):**
1. **Xác Suất Thắng/Thua**: Đưa ra % cụ thể (Ví dụ: "Khả năng thắng: 65%, Khả năng thua: 35%")
2. **Dự Toán Tiền**: Số tiền có thể thắng/thua (Ví dụ: "Nếu đặt 1 triệu, có thể thắng 2-4 triệu hoặc mất hết")
3. **Mức Độ Rủi Ro**: Thang điểm 1-10 (1=An toàn, 10=Cực kỳ nguy hiểm)
4. **Thời Điểm Tốt Nhất**: Giờ cụ thể (Ví dụ: "15h-17h hôm nay")
5. **Lời Khuyên Hành Động**: Nên/Không nên + Lý do cụ thể

TRẢ LỜI PHẢI CÓ CON SỐ CỤ THỂ, KHÔNG NÓI CHUNG CHUNG.
"""
        else:
            prompt = f"""Bạn là chuyên gia Kỳ Môn Độn Giáp hàng đầu.

**CHỦ ĐỀ:** {topic}
**CUNG:** {palace_data.get('num')} - {palace_data.get('sao')}/{palace_data.get('mon')}/{palace_data.get('than')}
{case_context}

**YÊU CẦU:**
1. **Khả Năng Thành Công**: % cụ thể
2. **Mức Độ Thuận Lợi**: Điểm 1-10
3. **Thời Điểm Tốt Nhất**: Ngày giờ cụ thể
4. **Rủi Ro Cần Tránh**: Liệt kê 2-3 điều với mức độ nguy hiểm
5. **Hành Động Cụ Thể**: 3 bước thực hiện ngay

ĐƯA RA CON SỐ VÀ THỜI GIAN CỤ THỂ.
"""
        
        return self._call_ai(prompt, use_hub=True, use_web_search=True)

    def summarize_with_depth(self, basic_analysis, topic):
        """Final polish: Adds depth, practical examples, and actionable advice."""
        prompt = f"""
Dựa trên luận giải gốc: {basic_analysis}
Hãy nâng tầm bài luận này cho chủ đề: **{topic}**.

YÊU CẦU NÂNG CẤP:
1. **Ví dụ cụ thể**: Đưa ra 2 ví dụ thực tế nếu hành động theo bản tin này (Cát) hoặc bỏ qua (Hung).
2. **Chiến lược thực thi**: Gợi ý 3 bước hành động cụ thể để tối ưu hóa kết quả.
3. **Độ sâu tri thức**: Kết nối với 1 nguyên lý âm dương ngũ hành sâu sắc liên quan đến chủ đề này.

Phong cách: Sắc bén, thực dụng, ngôn ngữ của một bậc thầy tư vấn cấp cao.
"""
        return self._call_ai(prompt, use_hub=True)

    def generate_quick_actions(self, analysis, topic):
        """Extracts 3-5 immediate, high-impact action steps."""
        prompt = f"""
Dựa trên luận giải: {analysis}
Hãy trích xuất RA NGAY 3-5 HÀNH ĐỘNG KHẨN CẤP và HIỆU QUẢ NHẤT cho chủ đề: **{topic}**.

YÊU CẦU:
1. **Ngắn gọn**: Mỗi hành động tối đa 1 dòng.
2. **Thực thi**: Phải là việc làm được ngay (Ví dụ: 'Gọi điện lúc 10h15', 'Đặt cây cảnh hướng Đông').
3. **Màu sắc**: Phân loại mức độ quan trọng (Cao, Trung bình, Thấp).

Trả lời dưới dạng danh sách gạch đầu dòng, không dẫn nhập.
"""
        return self._call_ai(prompt, use_hub=False)
    
    def analyze_palace(self, palace_data, topic):
        """
        Analyze a specific palace with SUPER INTELLIGENCE - Evidence-based with quantitative predictions
        """
        # Update context
        self.update_context(
            topic=topic,
            palace=palace_data,
            last_action=f"Phân tích Cung {palace_data.get('num')}"
        )
        
        # Classify topic for specialized analysis
        topic_type = self.classify_topic_intent(topic)
        
        # Search for evidence in knowledge hub
        evidence = self.search_knowledge_hub(topic, max_results=2)
        evidence_context = ""
        
        # FALLBACK: If hub is empty, search Google for real-world examples
        if not evidence or len(evidence) < 1:
            try:
                from ai_modules.web_searcher import get_web_searcher
                searcher = get_web_searcher()
                web_query = f"{topic} Kỳ Môn Độn Giáp ví dụ thực tế"
                web_results = searcher.search_google(web_query, num_results=3)
                if web_results:
                    evidence_context = "\n\n**VÍ DỤ THỰC TẾ TỪ GOOGLE:**\n"
                    for e in web_results[:2]:
                        evidence_context += f"- {e.get('title', 'N/A')}: {e.get('snippet', 'N/A')[:150]}...\n"
            except:
                pass
        else:
            evidence_context = "\n\n**CHỨNG CỨ TỪ KHO TRI THỨC:**\n"
            for e in evidence:
                evidence_context += f"- {e['title']}: {e['content_snippet'][:150]}...\n"
        
        context = self.get_context_prompt()
        
        # Super intelligence prompt with quantitative demands
        prompt = f"""{context}Bạn là Đại Pháp Sư Kỳ Môn Độn Giáp với 30 năm kinh nghiệm dự đoán chính xác.

**CHỦ ĐỀ:** {topic} (Loại: {topic_type})
**CUNG PHÂN TÍCH:** {palace_data.get('num', 'N/A')}
**CẤU HÌNH:**
- Sao: {palace_data.get('sao')}
- Môn: {palace_data.get('mon')}
- Thần: {palace_data.get('than')}
- Can Thiên: {palace_data.get('can_thien')}
- Can Địa: {palace_data.get('can_dia')}
- Hành: {palace_data.get('hanh')}
{evidence_context}

**YÊU CẦU SIÊU TRÍ TUỆ (BẮT BUỘC):**
1. **Đánh Giá Định Lượng**: Cung này thuận lợi bao nhiêu % cho "{topic}"? (Ví dụ: "Thuận lợi 75%")
2. **Dự Đoán Cụ Thể**: Nếu hành động theo cung này, kết quả sẽ như thế nào? (Phải có con số hoặc mô tả rõ ràng)
3. **Mức Độ Rủi Ro**: Điểm từ 1-10 (1=An toàn, 10=Cực nguy hiểm)
4. **Thời Điểm Tốt Nhất**: Giờ/ngày cụ thể để hành động
5. **Hành Động Ngay**: 2-3 việc làm được ngay lập tức

**QUAN TRỌNG:** Trả lời PHẢI CÓ CON SỐ, THỜI GIAN CỤ THỂ. Không nói chung chung kiểu "có thể", "nên cân nhắc". Hãy đưa ra dự đoán chính xác dựa trên cấu hình Kỳ Môn.

Trả lời ngắn gọn, đi thẳng vào vấn đề."""

        try:
            return self._call_ai(prompt, use_hub=True, use_web_search=True)
        except Exception as e:
            return f"❌ Lỗi khi gọi AI: {str(e)}\n\nVui lòng kiểm tra API key hoặc thử lại."
    
    def calculate_seasonal_vitality(self, palace_element, current_month):
        """
        Determine strength: Vượng, Tướng, Hưu, Tù, Tử.
        Standard seasonal rules:
        - Spring (1,2): Wood vượng, Fire tướng, Water hưu, Metal tù, Earth tử.
        - Summer (4,5): Fire vượng, Earth tướng, Wood hưu, Water tù, Metal tử.
        - Autumn (7,8): Metal vượng, Water tướng, Earth hưu, Fire tù, Wood tử.
        - Winter (10,11): Water vượng, Wood tướng, Metal hưu, Earth tù, Fire tử.
        - Four Seasons (3,6,9,12): Earth vượng, Metal tướng, Fire hưu, Wood tù, Water tử.
        """
        # Element of the month
        month_map = {
            1: "Mộc", 2: "Mộc", 3: "Thổ",
            4: "Hỏa", 5: "Hỏa", 6: "Thổ",
            7: "Kim", 8: "Kim", 9: "Thổ",
            10: "Thủy", 11: "Thủy", 12: "Thổ"
        }
        month_element = month_map.get(current_month, "Thổ")
        
        rules = {
            "Mộc": {"Mộc": "Vượng", "Hỏa": "Tướng", "Thủy": "Hưu", "Kim": "Tù", "Thổ": "Tử"},
            "Hỏa": {"Hỏa": "Vượng", "Thổ": "Tướng", "Mộc": "Hưu", "Thủy": "Tù", "Kim": "Tử"},
            "Thổ": {"Thổ": "Vượng", "Kim": "Tướng", "Hỏa": "Hưu", "Mộc": "Tù", "Thủy": "Tử"},
            "Kim": {"Kim": "Vượng", "Thủy": "Tướng", "Thổ": "Hưu", "Hỏa": "Tù", "Mộc": "Tử"},
            "Thủy": {"Thủy": "Vượng", "Mộc": "Tướng", "Kim": "Hưu", "Thổ": "Tù", "Hỏa": "Tử"}
        }
        
        return rules.get(month_element, {}).get(palace_element, "Bình")

    def comprehensive_analysis(self, chart_data, topic, dung_than_info=None, topic_hints="", subj_stem=None, obj_stem=None, subj_label="Bản thân"):
        """Expert Consultation with Synthesis and Color-Coding Logic."""
        import json
        from datetime import datetime
        curr_month = 1 # Update with real data if possible, default to Spring (Mộc)
        try: curr_month = datetime.now().month
        except: pass

        # Update context
        self.update_context(
            topic=topic,
            chart_data=chart_data,
            dung_than=dung_than_info or [],
            last_action=f"Tư vấn chuyên sâu cho {subj_label}"
        )
        
        truc_phu = chart_data.get('truc_phu_ten', 'N/A')
        truc_su = chart_data.get('truc_su_ten', 'N/A')
        
        # Determine actual actors for this session
        final_subj_stem = subj_stem if subj_stem else chart_data.get('can_ngay', 'N/A')
        final_obj_stem = obj_stem if obj_stem else chart_data.get('can_gio', 'N/A')
        
        # Mapping for human-centric roles
        role_map = {
            final_subj_stem: subj_label,
            # If the user is asking about someone else, Day Stem might still be "Bạn (Người hỏi)"
            chart_data.get('can_ngay'): "Bạn (Người hỏi)" if final_subj_stem != chart_data.get('can_ngay') else subj_label,
            final_obj_stem: "Đối tượng/Mục tiêu" if final_obj_stem != chart_data.get('can_gio') else "Đối tượng (Can Giờ)"
        }
        
        # 1. GROUP DATA BY PALACE
        palaces_of_interest = {} # {palace_num: {info}}
        
        def add_to_poi(p_num, label):
            if p_num not in palaces_of_interest:
                palaces_of_interest[p_num] = {
                    'labels': [],
                    'star': chart_data.get('thien_ban', {}).get(p_num, 'N/A'),
                    'door': chart_data.get('nhan_ban', {}).get(p_num, 'N/A'),
                    'deity': chart_data.get('than_ban', {}).get(p_num, 'N/A'),
                    'can_thien': chart_data.get('can_thien_ban', {}).get(p_num, 'N/A'),
                    'can_dia': chart_data.get('dia_can', {}).get(p_num, 'N/A'),
                    'hanh': CUNG_NGU_HANH.get(p_num, 'N/A'),
                    'void': p_num in chart_data.get('khong_vong', []),
                    'horse': p_num == chart_data.get('dich_ma')
                }
            if label not in palaces_of_interest[p_num]['labels']:
                palaces_of_interest[p_num]['labels'].append(label)

        # Scan all palaces for actors and Useful Gods
        for i in range(1, 10):
            can_thien_p = chart_data.get('can_thien_ban', {}).get(i)
            # 1. Check for Roles (Bản thân, Anh chị...)
            if can_thien_p in role_map:
                add_to_poi(i, role_map[can_thien_p])
            
            # 2. Check for Dụng Thần Topic
            if dung_than_info:
                for dt in dung_than_info:
                    door_val = chart_data.get('nhan_ban', {}).get(i)
                    if (chart_data.get('thien_ban', {}).get(i) == dt or 
                        door_val == dt or 
                        chart_data.get('than_ban', {}).get(i) == dt or 
                        can_thien_p == dt or
                        (dt.split(' (')[0] if ' (' in dt else dt) in [door_val, f"{door_val} Môn"]):
                        add_to_poi(i, dt)
        
        # 2. CONTEXTUAL PROMPT
        poi_desc = []
        from qmdg_data import KY_MON_DATA
        # Vitality check
        from datetime import datetime
        curr_month = datetime.now().month
        
        for p_num, info in palaces_of_interest.items():
            labels_str = ", ".join(info['labels'])
            void_str = " [📍 KHÔNG VONG - Sự việc bế tắc/Trống rỗng]" if info['void'] else ""
            horse_str = " [🐎 DỊCH MÃ - Sự chuyển dịch/Nhanh chóng]" if info['horse'] else ""
            p_name = CUNG_TEN.get(p_num, f"Cung {p_num}")
            
            # Seasonal Strength
            vit = self.calculate_seasonal_vitality(info['hanh'], curr_month)
            
            # Detailed Symbolism Lookup
            star_prop = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['CUU_TINH'].get(info['star'], {}).get('Tính_Chất', 'Bình')
            door_prop = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_MON'].get(info['door'] if " Môn" in info['door'] else f"{info['door']} Môn", {}).get('Luận_Đoán', 'Bình')
            deity_prop = KY_MON_DATA['DU_LIEU_DUNG_THAN_PHU_TRO']['BAT_THAN'].get(info['deity'], {}).get('Tính_Chất', 'Bình')
            can_prop = KY_MON_DATA['CAN_CHI_LUAN_GIAI'].get(info['can_thien'], {}).get('Tính_Chất', 'Bình')
            
            desc = (f"- **{p_name} (Cung {p_num})**: Đại diện cho **{labels_str}**.\n"
                    f"  + Thành phần: Sao {info['star']} ({star_prop}), Môn {info['door']} ({door_prop}), Thần {info['deity']} ({deity_prop}).\n"
                    f"  + Thiên Can: {info['can_thien']} ({can_prop}) lâm trên {info['can_dia']}.\n"
                    f"  + Trạng thái: {vit}, {info['hanh']}{void_str}{horse_str}.")
            poi_desc.append(desc)

        prompt = f"""{self.get_context_prompt()}Bạn là một Bậc Thầy Kỳ Môn Độn Giáp chuyên nghiệp. Hãy thực hiện LUẬN GIẢI CHI TIẾT NHÂN QUẢ cho **{subj_label}** về chủ đề: **{topic}**.

**NGUYÊN TẮC LUẬN GIẢI SIÊU VIỆT VÀ DỊCH NGHĨA THỰC TẾ:**
1. **Dịch nghĩa thực tế (Meaning Translation)**: Không chỉ liệt kê tính chất. 
   - Nếu có **Mã Tinh**: Trả lời rõ {subj_label} đi xa hay gần? Gấp hay từ từ?
   - Nếu có **Khai Môn**: Công việc mới là gì? Có quyền lực không? Tốt hay xấu?
   - Nếu có **Sinh Môn**: Có lợi nhuận không? Ngôi nhà/vốn đó thế nào?
   - Nếu có **Trực Phù/Thiên Tâm**: Có lãnh đạo bảo trợ hay người có tâm giúp đỡ không?
2. **Luận giải tổng hợp (Synthesis)**: Xâu chuỗi tất cả yếu tố đỏ/đen (Cát/Hung) trong cung. Nếu cung vượng và có nhiều cát tinh (màu đỏ) thì phán quyết đại cát.
3. **Ví dụ thực tế**: BẮT BUỘC đưa ra ít nhất 1 ví dụ cụ thể về tình huống tương tự có thể xảy ra trong đời thực cho chủ đề "{topic}".
4. **Hành động sâu**: Gợi ý tư duy hoặc thái độ cần có để chuyển Hung thành Cát.
5. **Ngôn ngữ nhân văn**: Luôn dùng đúng danh xưng **"{subj_label}"**.

**DỮ LIỆU CÁC CUNG QUAN TRỌNG:**
{chr(10).join(poi_desc)}

**THẾ TRẬN TỔNG QUAN:**
- Xu thế (Trực Phù): {truc_phu}
- Chấp hành (Trực Sử): {truc_su}
- Gợi ý định hướng: "{topic_hints}"

Trả lời bằng phong thái chuyên gia tư vấn tận tâm, ngôn ngữ giàu hình ảnh và sắc bén."""

        try:
            return self._call_ai(prompt)
        except Exception as e:
            return f"❌ Lỗi khi gọi AI: {str(e)}"
    
    def analyze_mai_hoa(self, mai_hoa_res, topic="Chung"):
        """
        Analyze Mai Hoa Dich So data with AI
        """
        # Determine The/Dung
        if mai_hoa_res['dong_hao'] <= 3:
            the_quai = mai_hoa_res['upper']
            dung_quai = mai_hoa_res['lower']
            the_name = "Thượng Quái"
            dung_name = "Hạ Quái (Động)"
        else:
            the_quai = mai_hoa_res['lower']
            dung_quai = mai_hoa_res['upper']
            the_name = "Hạ Quái"
            dung_name = "Thượng Quái (Động)"
            
        the_element = QUAI_ELEMENTS.get(the_quai, "N/A")
        dung_element = QUAI_ELEMENTS.get(dung_quai, "N/A")
        
        prompt = f"""Bạn là bậc thầy Mai Hoa Dịch Số. Hãy luận giải quẻ này cho việc: **{topic}**.

**DỮ LIỆU QUẺ:**
- **Quẻ Chủ**: {mai_hoa_res['ten']} ({mai_hoa_res['upper_symbol']} trên {mai_hoa_res['lower_symbol']})
- **Hào Động**: Hào {mai_hoa_res['dong_hao']}
- **Quẻ Hỗ**: {mai_hoa_res['ten_ho']}
- **Quẻ Biến**: {mai_hoa_res['ten_qua_bien']}

**THẾ/DỤNG:**
- **Thể (Bản thân/Chủ thể)**: {QUAI_NAMES[the_quai]} (Hành {the_element}) - Tại {the_name}
- **Dụng (Sự việc/Đối tượng)**: {QUAI_NAMES[dung_quai]} (Hành {dung_element}) - Tại {dung_name}

**YÊU CẦU LUẬN GIẢI:**
1. **Tương quan Thể Dụng**: Hành của Thể và Dụng sinh khắc thế nào? (Thể khắc Dụng, Dụng sinh Thể là tốt; Thể sinh Dụng, Dụng khắc Thể là xấu).
2. **Ý nghĩa Quẻ Chủ, Hỗ, Biến**: 
    - Quẻ Chủ báo hiệu giai đoạn đầu.
    - Quẻ Hỗ báo hiệu diễn biến trung gian.
    - Quẻ Biến báo hiệu kết quả cuối cùng.
3. **Lời khuyên**: Hành động thế nào cho thuận theo quẻ?

**PHONG CÁCH**: Chuyên nghiệp, súc tích, giàu triết lý nhưng thực tế. Trả lời rõ ràng Cát hay Hung."""

        try:
            return self._call_ai(prompt)
        except Exception as e:
            return f"❌ Lỗi khi gọi AI: {str(e)}"
    
    def analyze_luc_hao(self, luc_hao_res, topic="Chung"):
        """
        Analyze Luc Hao (I Ching) data with AI. 
        Takes the result dictionary from luc_hao_kinh_dich.py
        """
        ban = luc_hao_res.get('ban', {})
        bien = luc_hao_res.get('bien', {})
        dong_hao = luc_hao_res.get('dong_hao', [])
        
        # Format details for Original Hexagram
        hào_details_ban = []
        for d in reversed(ban.get('details', [])):
            hào_details_ban.append(
                f"Hào {d['hao']}{d.get('marker', '')}: {d['luc_than']} - {d['can_chi']} - {d['luc_thu']} "
                f"({'ĐỘNG' if d['is_moving'] else 'tĩnh'})"
            )
        
        prompt = f"""Bạn là bậc thầy Lục Hào Kinh Dịch. Hãy luận giải quẻ này cho việc: **{topic}**.

**DỮ LIỆU QUẺ:**
- **Quẻ Chủ**: {ban.get('name')} (Họ {ban.get('palace')})
- **Quẻ Biến**: {bien.get('name')}
- **Hào Động**: {', '.join(map(str, dong_hao)) if dong_hao else 'Không có'}
- **Thế/Ứng**: {luc_hao_res.get('the_ung')}

**CHI TIẾT CÁC HÀO (Quẻ Chủ):**
{chr(10).join(hào_details_ban)}

**YÊU CẦU LUẬN GIẢI:**
1. **Dụng Thần**: Xác định Hào nào là Dụng Thần cho việc {topic}? Trạng thái của Dụng Thần (Vượng/Tướng/Hưu/Tù/Tử)?
2. **Sự Biến Hóa**: Hào động biến thành gì ở Quẻ Biến? Sự biến hóa này là "Hồi đầu sinh", "Hồi đầu khắc", hay "Hóa tiến", "Hóa thoái"?
3. **Kết luận**: Việc {topic} sẽ có diễn biến thế nào? Kết quả cuối cùng là Cát hay Hung?
4. **Lời khuyên**: Cần làm gì hoặc lưu ý điều gì?

**PHONG CÁCH**: Chuyên nghiệp, sắc bén, đi sâu vào mối quan hệ Sinh - Khắc giữa các hào và quẻ biến. Hãy luận giải CHI TIẾT quẻ biến."""

        try:
            return self._call_ai(prompt)
        except Exception as e:
            return f"❌ Lỗi khi gọi AI: {str(e)}"
    
    def answer_question(self, question, chart_data=None, topic=None):
        """
        Answer with FULL CONTEXT AWARENESS
        """
        # Use stored context if not provided
        if chart_data is None:
            chart_data = self.current_context.get('chart_data')
        if topic is None:
            topic = self.current_context.get('topic', 'Chung')
        
        # Update context
        self.update_context(
            topic=topic,
            chart_data=chart_data,
            last_action=f"Hỏi: {question[:50]}..."
        )
        
        context = self.get_context_prompt()
        
        # Build chart context if available
        chart_context = ""
        if chart_data:
            palace_summary = []
            for i in range(1, 10):
                palace_summary.append(
                    f"Cung {i}: {chart_data.get('thien_ban', {}).get(i, 'N/A')} - "
                    f"{chart_data.get('nhan_ban', {}).get(i, 'N/A')} - "
                    f"{chart_data.get('than_ban', {}).get(i, 'N/A')}"
                )
            chart_context = "\n**Bàn Kỳ Môn hiện tại:**\n" + "\n".join(palace_summary)
        
        prompt = f"""{context}Bạn là chuyên gia Kỳ Môn Độn Giái.

**Bối cảnh:**
- Chủ đề: {topic}
{chart_context}

**Câu hỏi của người dùng:**
{question}

Hãy trả lời câu hỏi dựa trên:
1. Ngữ cảnh hiện tại (chủ đề, cung đang xem, hành động trước)
2. Thông tin từ bàn Kỳ Môn (nếu có)
3. Kiến thức về dịch học
4. Nguyên lý Ngũ hành, Bát quái

Trả lời CỰC KỲ NGẮN GỌN (tối đa 3-5 câu), tập trung vào thực tế, không lý thuyết suông."""

        try:
            return self._call_ai(prompt)
        except Exception as e:
            return f"❌ Lỗi: {str(e)}"
    
    def explain_element(self, element_type, element_name):
        """
        Explain element with context
        """
        # Update context
        self.update_context(
            last_action=f"Giải thích {element_type}: {element_name}"
        )
        
        context = self.get_context_prompt()
        
        type_map = {
            'star': 'Tinh (Sao)',
            'door': 'Môn (Cửa)',
            'deity': 'Thần',
            'stem': 'Can (Thiên Can)'
        }
        
        prompt = f"""{context}Bạn là chuyên gia Kỳ Môn Độn Giái.

Hãy giải thích CỐT LÕI về {type_map.get(element_type, element_type)}: **{element_name}**

**Yêu cầu (Tối đa 3-4 dòng):**
1. Bản chất cốt lõi (Cát/Hung/Ngũ hành).
2. Tác động chính đến vận mệnh/công việc.
3. Lời khuyên nhanh khi gặp yếu tố này.

Bỏ qua nguồn gốc, ví dụ hay dẫn giải dài dòng. Trả lời sắc bén, súc tích."""

        try:
            return self._call_ai(prompt)
        except Exception as e:
            return f"❌ Lỗi: {str(e)}"

# Compatibility Alias
GeminiQMDGHelper = GeminiQMDGHelperV172

# Helper variables
QUAI_NAMES = {1: "Khảm", 2: "Khôn", 3: "Chấn", 4: "Tốn", 6: "Càn", 7: "Đoài", 8: "Cấn", 9: "Ly"}
QUAI_ELEMENTS = {1: "Thủy", 2: "Thổ", 3: "Mộc", 4: "Mộc", 6: "Kim", 7: "Kim", 8: "Thổ", 9: "Hỏa"}
