import os
import json
from datetime import datetime
from unittest.mock import patch
from free_ai_helper import FreeAIHelper
from luc_hao_kinh_dich import lap_qua_luc_hao
from qmdg_calc import calculate_qmdg_params

def run_test():
    helper = FreeAIHelper()
    
    # Fake chart data
    chart_data = {
        'can_nam': 'Bính', 'chi_nam': 'Ngọ',
        'can_thang': 'Canh', 'chi_thang': 'Dần',
        'can_ngay': 'Nhâm', 'chi_ngay': 'Thìn',
        'can_gio': 'Ất', 'chi_gio': 'Tị'
    }
    
    # Run Luc Hao
    luc_hao = lap_qua_luc_hao(
        2026, 2, 15, 10,
        topic="Tình duyên",
        can_ngay="Nhâm", chi_ngay="Thìn",
        can_thang="Canh", chi_thang="Dần"
    )
    
    # Run Ky Mon
    dt_test = datetime(2026, 2, 15, 10, 0)
    ky_mon = calculate_qmdg_params(dt_test)
    
    question = "Mối quan hệ tình cảm sắp tới của tôi sẽ ra sao?"
    
    offline_output = []
    online_prompt = []
    
    # Patch _try_online_ai to capture the prompt
    original_try_online_ai = helper._try_online_ai
    def mock_try_online_ai(*args, **kwargs):
        # We can't easily capture the prompt if it's deeply nested, but let's mock _call_ai instead.
        pass
        
    with patch.object(helper, '_call_ai', side_effect=lambda prompt, **kwargs: prompt):
        # By mocking _call_ai to return the prompt, answer_question will return the prompt as if it was the answer!
        # Wait, if we force the API key to be "test", it will try online.
        os.environ["GEMINI_API_KEY"] = "fake_key_for_test"
        helper.api_key = "fake_key_for_test"
        online_result = helper.answer_question(question, chart_data=chart_data, luc_hao_data=luc_hao, ky_mon_data=ky_mon)
        online_prompt.append(online_result)

    with patch.object(helper, 'api_key', None):
        os.environ.pop("GEMINI_API_KEY", None)
        offline_result = helper.answer_question(question, chart_data=chart_data, luc_hao_data=luc_hao, ky_mon_data=ky_mon)
        offline_output.append(offline_result)

    # Ghi log ra file để audit
    with open("test_output2.txt", "w", encoding="utf-8") as f:
        f.write("=== LOG KIỂM THỬ FREE_AI_HELPER V42.9 ===\n")
        f.write(offline_output[0] + "\n\n")
        
        f.write("=== ONLINE PROMPT (WHAT GEMINI SEES) ===\n")
        f.write(str(online_prompt[0]) + "\n\n")

if __name__ == "__main__":
    run_test()
