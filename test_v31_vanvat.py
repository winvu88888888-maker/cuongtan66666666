import sys
sys.path.insert(0, r'C:\Users\GHC\.gemini\antigravity\scratch\cuongtan66666666_fix')
from van_vat_chi_tiet import format_van_vat_for_ai, get_tham_tu_mo_ta

# Test: Kim + Mộ (vật kim loại nhỏ cũ bị chôn)
print(format_van_vat_for_ai('Kim', 'Mộ'))
print()
print(get_tham_tu_mo_ta('Kim', 'Mộ', 'trên tay tôi cầm vật gì'))
print()
print("="*60)
# Test: Hỏa + Đế Vượng (vật phát sáng cực lớn)
print(format_van_vat_for_ai('Hỏa', 'Đế Vượng'))
print()
print("="*60)
# Test: Thủy + Tử (nước hỏng/cạn)
print(format_van_vat_for_ai('Thủy', 'Tử'))
