
import qmdg_calc
from datetime import datetime

print("Testing qmdg_calc for Horse/Void data...")
now = datetime.now()
params = qmdg_calc.calculate_qmdg_params(now)

print(f"Time: {now}")
print(f"Can/Chi: {params['can_nam']} {params['chi_nam']}, {params['can_thang']} {params['chi_thang']}, {params['can_ngay']} {params['chi_ngay']}, {params['can_gio']} {params['chi_gio']}")

print("\nHORSE DATA (ma):")
print(params['ma'])

print("\nVOID DATA (khong):")
print(params['khong'])

# Validation
for key in ['nam', 'thang', 'ngay', 'gio']:
    ma_val = params['ma'].get(key)
    khong_val = params['khong'].get(key)
    print(f"{key.upper()}: Ma={ma_val} ({type(ma_val)}), Khong={khong_val} ({type(khong_val)})")
