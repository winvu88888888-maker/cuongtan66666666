import re

print('=== ĐẠI LỤC NHÂM ELEMENTS (dai_luc_nham.py) ===')
with open('dai_luc_nham.py', 'r', encoding='utf-8') as f:
    dln = f.read()
for term in ['Sơ Truyền','Trung Truyền','Mạt Truyền','Thiên Bàn','Địa Bàn','Quý Nhân','Đằng Xà','Chu Tước','Lục Hợp','Câu Trận','Thanh Long','Thiên Không','Bạch Hổ','Thái Thường','Huyền Vũ','Thái Âm','Thiên Hậu','Tam Truyền','Tứ Khóa','Sơ Khóa','Trung Khóa','Mạt Khóa','Lưu Niên Khóa']:
    c = dln.count(term)
    mark = 'OK' if c > 0 else 'MISS'
    print(f'  [{mark}] {term}: {c}')

print()
print('=== THÁI ẤT ELEMENTS (thai_at_than_so.py) ===')
with open('thai_at_than_so.py', 'r', encoding='utf-8') as f:
    ta = f.read()
for term in ['Thái Ất','Cửu Cung','Ngũ Phúc','Thiên Mục','Địa Mục','Chủ Toán','Khách Toán','Thái Ất Tích','Trung Thiên','Thiên Bàn','Địa Bàn','Cung Thân','Cung Mệnh']:
    c = ta.count(term)
    mark = 'OK' if c > 0 else 'MISS'
    print(f'  [{mark}] {term}: {c}')

print()
print('=== THIẾT BẢN ELEMENTS ===')
with open('free_ai_helper.py', 'r', encoding='utf-8') as f:
    fah = f.read()
for term in ['Thiết Bản','Thần Số','Lạc Thư','Hà Đồ','Cửu Cung','Bát Quái']:
    c = fah.count(term)
    mark = 'OK' if c > 0 else 'MISS'
    print(f'  [{mark}] {term}: {c}')
