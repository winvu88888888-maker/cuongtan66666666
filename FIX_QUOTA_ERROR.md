# 🚨 HƯỚNG DẪN SỬA LỖI 429 QUOTA EXCEEDED

## ⚠️ VẤN ĐỀ

Bạn đang gặp lỗi:
```
429 You exceeded your current quota
Quota exceeded for metric: gemini-2.5-pro
```

**Nguyên nhân:**
- API Key đã HẾT QUOTA miễn phí hàng ngày cho model `gemini-2.5-pro`
- Model **Pro** tốn quota **rất nhiều** (~10 lần so với Flash)
- Quota miễn phí của Google: **Rất hạn chế** cho Pro models

---

## ✅ GIẢI PHÁP ĐÃ ÁP DỤNG (TRONG CODE MỚI)

### 1. Thay Đổi Ưu Tiên Model

**TRƯỚC (Cũ - TỐN QUOTA):**
```python
models_to_try = [
    'gemini-2.0-flash-exp',
    'gemini-1.5-pro-latest',  # ← Model Pro tốn quota nhiều
    'gemini-1.5-pro',          # ← Model Pro tốn quota nhiều
    'gemini-1.5-flash-latest',
]
```

**SAU (Mới - TIẾT KIỆM QUOTA):**
```python
models_to_try = [
    # Ưu tiên FLASH trước (tiết kiệm quota x10)
    'gemini-2.5-flash',
    'gemini-2.5-flash-preview-09-2025',
    'gemini-2.5-flash-lite',
    'gemini-2.0-flash',
    'gemini-1.5-flash-latest',
    
    # Chỉ dùng Pro khi Flash không khả dụng
    'gemini-1.5-pro-latest',
    'gemini-1.5-pro',
]
```

### 2. Tự Động Retry Khi Gặp Quota Error

Code đã được cập nhật để:
- ✅ **Tự động phát hiện** lỗi quota (429)
- ✅ **Chuyển sang model khác** ngay lập tức  
- ✅ **Lưu cache model bị lỗi** để không thử lại
- ✅ **Hiển thị thông báo rõ ràng** cho người dùng

---

## 🔧 CÁCH SỬA NGAY (3 TÙY CHỌN)

### TÙY CHỌN 1: Chạy Code Mới (KHUYẾN NGHỊ)

1. **Chạy script push** (code đã sửa):
   ```
   C:\Users\GHC\Desktop\python1 - Copy\UPLOAD_TO_STREAMLIT\push_fix_quota.bat
   ```

2. **Chờ Streamlit Cloud deploy** (1-2 phút)

3. **Refresh web app**: https://cuongtan66666666.streamlit.app/

4. **Kiểm tra** - Lỗi sẽ biến mất, app sẽ dùng model Flash

### TÙY CHỌN 2: Tạo API Key Mới  

1. **Truy cập**: https://aistudio.google.com/app/apikey

2. **Đăng nhập tài khoản Google KHÁC** (nếu có)
   - Hoặc tạo project mới trong cùng tài khoản

3. **Click "Create API Key"** → Copy key mới

4. **Cập nhật trên Streamlit Cloud**:
   - Vào Settings → Secrets
   - Thay API Key cũ bằng key mới:
   ```toml
   GEMINI_API_KEY = "YOUR_NEW_API_KEY_HERE"
   ```
   - Save

### TÙY CHỌN 3: Chờ Quota Reset (Ít Khuyến Nghị)

- Quota miễn phí reset mỗi **24 giờ**
- Nhưng với usage hiện tại của bạn, sẽ hết quota rất nhanh

---

## 📊 SO SÁNH FLASH VS PRO

| Tiêu chí | Gemini Flash | Gemini Pro |
|----------|--------------|------------|
| **Quota tiêu thụ** | 1x (Tiêu chuẩn) | ~10x (Rất cao) |
| **Tốc độ** | ⚡ Rất nhanh | 🐌 Chậm hơn |
| **Chi phí** | 💰 Rẻ/Miễn phí | 💰💰💰 Đắt |
| **Độ thông minh** | 🧠 90% Pro | 🧠 100% |
| **Phù hợp cho** | Hầu hết use cases | Phân tích phức tạp |

**KẾT LUẬN:** 
- ✅ Với ứng dụng Kỳ Môn Độn Giáp, **Flash là đủ**
- ✅ Flash **tiết kiệm quota** gấp 10 lần
- ✅ Tốc độ **nhanh hơn** → UX tốt hơn

---

## 🔍 KIỂM TRA QUOTA HIỆN TẠI

1. **Truy cập**: https://ai.dev/rate-limit

2. **Đăng nhập** với tài khoản dùng API Key

3. **Xem usage**:
   - gemini-2.5-pro: **0/0** (Hết quota) ❌
   - gemini-2.5-flash: **xxx/yyy** (Còn quota) ✅

---

## 🛠️ DEBUG STEPS

Nếu sau khi deploy code mới VẪN gặp lỗi:

### Bước 1: Xác Nhận Code Đã Deploy

1. Vào GitHub: https://github.com/winvu88888888-maker/cuongtan66666666

2. Kiểm tra file `gemini_helper.py` dòng ~118

3. Xem có dòng này không:
   ```python
   'gemini-2.5-flash',  # ← Phải là model đầu tiên
   ```

### Bước 2: Kiểm Tra Streamlit Cloud

1. Vào: https://share.streamlit.io/

2. Click app → **Logs**

3. Xem model nào đang được sử dụng:
   ```
   Trying model: gemini-2.5-flash  ← ĐÚNG
   hoặc
   Trying model: gemini-2.5-pro    ← SAI (chưa deploy)
   ```

### Bước 3: Force Restart App

1. Trong Streamlit Cloud Dashboard

2. Click **⋮** (3 chấm) → **Reboot app**

3. Chờ 30 giây → Refresh

---

## 📝 FILE LIÊN QUAN

Các file đã được sửa:

1. **`gemini_helper.py`** (dòng 112-138)
   - Thay đổi thứ tự ưu tiên model

2. **`app.py`** (dòng 937-970)
   - Cải thiện logic lấy API key
   - Thêm cảnh báo thiếu secret

3. **`push_fix_quota.bat`** (MỚI)
   - Script push code tự động

---

## 💡 KHUYẾN NGHỊ DÀI HẠN

### 1. Luôn Dùng Flash Cho Production

- Tiết kiệm quota
- Tốc độ nhanh hơn
- Độ chính xác vẫn rất cao (~90% so với Pro)

### 2. Chỉ Dùng Pro Khi Thật Sự Cần

Ví dụ:
- Phân tích cực kỳ phức tạp
- Cần độ chính xác tuyệt đối
- Xử lý văn bản dài (>100K tokens)

### 3. Set Up Monitoring

Tạo cảnh báo khi:
- Quota còn < 20%
- Gặp lỗi 429

### 4. Tạo Nhiều API Keys Backup

- Tài khoản Google 1: Key A (Primary)
- Tài khoản Google 2: Key B (Backup)
- Tài khoản Google 3: Key C (Emergency)

---

## 🆘 VẪN CÒN LỖI?

Nếu sau khi làm theo tất cả bước trên vẫn lỗi:

1. **Chụp ảnh lỗi** đầy đủ

2. **Export Streamlit Logs**:
   - Settings → Logs → Download

3. **Kiểm tra**:
   - Model nào đang được dùng?
   - Quota còn bao nhiêu?
   - Secret đã set chưa?

4. **Liên hệ** với thông tin trên

---

**Tác giả:** Vũ Việt Cường  
**Email:** winvu88888888@gmail.com  
**Web:** https://cuongtan66666666.streamlit.app/
