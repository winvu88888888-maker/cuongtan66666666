# 🌐 Hướng Dẫn Cấu Hình API Key Trên Streamlit Cloud

## ⚠️ VẤN ĐỀ

Nếu bạn thấy lỗi **"API Key không hoạt động"** trên web https://cuongtan888888.streamlit.app/, đó là vì **chưa cấu hình Secret trên Streamlit Cloud**.

> **LƯU Ý QUAN TRỌNG**: File `.streamlit/secrets.toml` trong code chỉ dùng cho local. Khi deploy lên Streamlit Cloud, bạn PHẢI cấu hình riêng trên Dashboard.

---

## ✅ CÁCH SỬA (2 PHÚT)

### Bước 1: Truy Cập Streamlit Cloud Dashboard

1. Đăng nhập vào: **https://share.streamlit.io/**
   - Dùng email: **winvu88888888@gmail.com**

2. Tìm ứng dụng có tên: **cuongtan888888** hoặc **cuongtan888888.streamlit.app**

### Bước 2: Cấu Hình Secret

1. Click vào app của bạn

2. Click vào biểu tượng **⚙️ Settings** (góc phải màn hình)

3. Chọn tab **"Secrets"** (ở menu bên trái)

4. **Xóa toàn bộ** nội dung cũ (nếu có)

5. **Dán đoạn code sau** vào ô Secret:

```toml
GEMINI_API_KEY = "AIzaSyDv_tCfjrTOXSNQhtKSneaFlyrM7RVp9Ow"
```

6. Click nút **"Save"** ở góc dưới

7. **Chờ 30-60 giây** để app tự động restart

### Bước 3: Kiểm Tra Lại

1. Vào lại web: https://cuongtan888888.streamlit.app/

2. Kiểm tra sidebar, phần **"🤖 Cấu hình AI"**

3. Bạn sẽ thấy:
   - ✅ **"Gemini Pro (V1.7.5)"** → API key đã hoạt động
   - ❌ **"Free AI (Offline Mode)"** hoặc cảnh báo đỏ → Cần kiểm tra lại

---

## 🔍 KIỂM TRA API KEY CÓ ĐÚNG KHÔNG?

Nếu sau khi cấu hình vẫn lỗi, hãy kiểm tra API key:

1. Truy cập: https://aistudio.google.com/app/apikey
2. Đăng nhập bằng tài khoản Google của bạn
3. Kiểm tra xem API Key có còn hoạt động không
4. Nếu cần, tạo API Key mới và cập nhật lại vào Streamlit Secrets

**API Key hiện tại của bạn:**
```
AIzaSyDv_tCfjrTOXSNQhtKSneaFlyrM7RVp9Ow
```

---

## 📋 CHECKLIST SỬA LỖI

- [ ] Đã đăng nhập vào Streamlit Cloud Dashboard
- [ ] Đã tìm thấy app **cuongtan888888**
- [ ] Đã vào **Settings → Secrets**
- [ ] Đã dán đúng format: `GEMINI_API_KEY = "YOUR_KEY"`
- [ ] Đã click **Save**
- [ ] Đã chờ app restart (30-60 giây)
- [ ] Đã F5 refresh lại trang web
- [ ] Sidebar hiển thị **"Gemini Pro (V1.7.5)"**

---

## 🆘 NẾU VẪN LỖI

### Lỗi 1: "API_KEY_INVALID"
→ API Key không đúng hoặc đã hết hạn  
→ Tạo API Key mới tại: https://aistudio.google.com/app/apikey

### Lỗi 2: "No module named 'google.generativeai'"
→ Thiếu thư viện trong requirements.txt  
→ Kiểm tra file `requirements.txt` có dòng: `google-generativeai>=0.8.0`

### Lỗi 3: Vẫn hiện "Free AI (Offline Mode)"
→ Secret chưa được lưu đúng cách  
→ Thử xóa secret cũ → Dán lại → Save → Restart app

### Lỗi 4: Quota Exceeded
→ API Key đã hết quota miễn phí  
→ Chờ reset (mỗi ngày) hoặc tạo API Key mới

---

## 💡 TIPS

1. **Format phải CHÍNH XÁC**:
   - Đúng: `GEMINI_API_KEY = "AIza..."`
   - Sai: `GEMINI_API_KEY: "AIza..."` (dùng dấu hai chấm)
   - Sai: `GEMINI_API_KEY = AIza...` (thiếu dấu ngoặc kép)

2. **Không có khoảng trắng thừa**:
   - Đúng: `GEMINI_API_KEY = "key"`
   - Sai: `GEMINI_API_KEY  =  "key"` (khoảng trắng thừa)

3. **Chờ app restart hoàn toàn** trước khi kiểm tra lại

---

## 📞 LIÊN HỆ

Nếu làm theo hướng dẫn mà vẫn lỗi, vui lòng cung cấp:
1. Screenshot phần Secrets trên Streamlit Cloud
2. Screenshot lỗi trên web app
3. Thời gian xảy ra lỗi

**Tác giả:** Vũ Việt Cường  
**Email:** winvu88888888@gmail.com
