import free_ai_helper as fp
f = fp.FreeAIHelper()
from test_v24_audit import chart_data, luc_hao_data, mai_hoa_data

print("-----")
try:
    print("KM:", f._ky_mon_scoring(chart_data, 'Thê Tài'))
except Exception as e:
    import traceback; traceback.print_exc()

try:
    print("LH:", f._luc_hao_scoring(luc_hao_data, 'Thê Tài'))
except Exception as e:
    import traceback; traceback.print_exc()

try:
    print("MH:", f._mai_hoa_scoring(mai_hoa_data, chart_data))
except Exception as e:
    import traceback; traceback.print_exc()

try:
    print("TB:", f._thiet_ban_scoring(chart_data, luc_hao_data, mai_hoa_data))
except Exception as e:
    import traceback; traceback.print_exc()

try:
    print("LN:", f._luc_nham_scoring(chart_data))
except Exception as e:
    import traceback; traceback.print_exc()

try:
    print("TA:", f._thai_at_scoring(chart_data))
except Exception as e:
    import traceback; traceback.print_exc()
