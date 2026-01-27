# 🤖 Hướng Dẫn Sử Dụng Gemini AI Trong Web App

## 🎯 Tổng Quan

Web app Kỳ Môn Độn Giáp đã tích hợp **Gemini AI** - trợ lý AI thông minh giúp bạn:
- 🔮 Phân tích chi tiết từng cung
- 📖 Giải thích ý nghĩa các yếu tố (Sao, Môn, Thần, Can)
- 💬 Trả lời câu hỏi về Kỳ Môn và dịch học
- 📊 Phân tích tổng hợp toàn bộ bàn

---

## 🔑 Bước 1: Lấy Gemini API Key (MIỄN PHÍ)

### Cách Lấy API Key

1. **Truy cập trang tạo API key:**
   👉 **[Bấm vào đây để lấy API Key](https://aistudio.google.com/app/apikey)**

2. **Đăng nhập Google:**
   - Sử dụng tài khoản Google của bạn
   - Chấp nhận điều khoản sử dụng

3. **Tạo API Key:**
   - Click nút **"Create API Key"** hoặc **"Get API Key"**
   - Chọn project (hoặc tạo mới)
   - Copy API key (dạng: `AIzaSy...`)

4. **Lưu ý:**
   - ✅ API key hoàn toàn **MIỄN PHÍ**
   - ✅ Có hạn mức sử dụng hàng ngày (đủ dùng)
   - ⚠️ **KHÔNG chia sẻ** API key với người khác
   - ⚠️ **KHÔNG đăng** API key lên mạng xã hội

---

## ⚙️ Bước 2: Kích Hoạt Gemini Trên Web App

### Cách Nhập API Key

1. **Mở web app:**
   - Truy cập: `https://cuongtan12345678.streamlit.app/`
   - Nhập mật khẩu: `1987`

2. **Tìm phần cấu hình:**
   - Mở **Sidebar** (thanh bên trái)
   - Tìm phần **"🔑 Nhập Gemini API Key"**

3. **Nhập API key:**
   - Dán API key vào ô input
   - Click nút **"Kích hoạt Gemini Ngay"**
   - Đợi thông báo **"✅ Đã kích hoạt Gemini!"**

4. **Kiểm tra trạng thái:**
   - Xem dòng: **"🤖 Trạng thái AI: Gemini Pro (Active)"**
   - Nếu thấy dòng này → ✅ Thành công!

---

## 🚀 Bước 3: Sử Dụng Các Tính Năng AI

### 3.1 Phân Tích Cung 🔮

**Cách dùng:**
1. Chọn chủ đề (ví dụ: "Tình Cảm", "Tài Lộc")
2. Xem bàn 9 cung
3. Click vào **"📖 Chi tiết Cung X"** (expander)
4. Click nút **"🤖 Hỏi AI về Cung X"**
5. Đợi AI phân tích

**AI sẽ cho bạn:**
- Ý nghĩa tổng quan của cung
- Phân tích từng yếu tố (Sao, Môn, Thần, Can)
- Tương tác giữa các yếu tố
- Điềm báo (cát/hung)
- Lời khuyên cụ thể

### 3.2 Giải Thích Yếu Tố 📖

**Cách dùng:**
1. Trong phần chi tiết cung
2. Tìm các nút:
   - **"🤖 Giải thích [Tên Sao]"**
   - **"🤖 Giải thích [Tên Môn]"**
   - **"🤖 Giải thích [Tên Thần]"**
   - **"🤖 Giải thích [Can/Can]"**
3. Click nút tương ứng
4. Đọc giải thích chi tiết từ AI

**AI sẽ giải thích:**
- Nguồn gốc và ý nghĩa
- Thuộc tính (Ngũ hành, âm dương)
- Tính chất (cát/hung)
- Ứng dụng trong luận đoán
- Ví dụ cụ thể

### 3.3 Hỏi Đáp AI 💬

**Cách dùng:**
1. Chọn tab **"🤖 Hỏi Gemini AI"** trong sidebar
2. Hoặc cuộn xuống phần **"💬 Hỏi Đáp AI"**
3. Nhập câu hỏi vào ô chat
4. Click **"Gửi"** hoặc Enter
5. Đợi AI trả lời

**Ví dụ câu hỏi:**
- "Cung 1 có ý nghĩa gì trong tình cảm?"
- "Thiên Phụ Tinh là sao gì?"
- "Khai Môn tốt hay xấu?"
- "Làm sao biết thời điểm tốt để khởi sự?"
- "Giải thích về Ngũ hành sinh khắc?"

### 3.4 Phân Tích Tổng Hợp 📊

**Cách dùng:**
1. Cuộn xuống phần **"📋 BÁO CÁO TỔNG HỢP"**
2. Click **"🎯 Tạo Báo Cáo Tổng Hợp"**
3. Đợi AI phân tích toàn bộ bàn
4. Xem kết quả chi tiết

**AI sẽ phân tích:**
- Tổng quan tình hình
- Các điểm mạnh/yếu
- Tương tác giữa các cung
- Thời điểm tốt/xấu
- Lời khuyên tổng hợp
- Dự đoán kết quả

---

## 🆓 Chế Độ Free AI (Không Cần API Key)

Nếu **không có** Gemini API key, web app vẫn hoạt động với **Free AI Mode**:

### Tính Năng Free AI
- ✅ Phân tích cơ bản dựa trên database
- ✅ Giải thích các yếu tố theo kiến thức có sẵn
- ✅ Luận đoán theo quy tắc Kỳ Môn
- ⚠️ **KHÔNG** có khả năng suy luận thông minh như Gemini
- ⚠️ **KHÔNG** có ngữ cảnh và phân tích sâu

### Khi Nào Dùng Free AI?
- Khi chưa có API key
- Khi hết hạn mức Gemini
- Khi muốn phân tích nhanh, đơn giản

---

## 🔗 Tính Năng Nâng Cao: n8n Integration (Optional)

### n8n Là Gì?
- Công cụ tự động hóa workflow
- Cho phép dùng **Gemini 1.5 Pro** (model tốt nhất)
- Monitoring và logging

### Cách Cấu Hình n8n

1. **Cài đặt n8n:**
   ```bash
   npm install -g n8n
   n8n start
   ```

2. **Import workflow:**
   - Mở n8n: `http://localhost:5678`
   - Import file: `n8n_workflows/gemini_expert.json`
   - Kích hoạt workflow

3. **Lấy Webhook URL:**
   - Copy URL webhook (dạng: `http://localhost:5678/webhook/gemini-expert`)

4. **Nhập vào web app:**
   - Mở sidebar
   - Tìm phần **"🔗 Kết nối n8n (Best Gemini)"**
   - Dán webhook URL
   - ✅ Xong!

### Lợi Ích n8n
- ✅ Sử dụng Gemini 1.5 Pro (thông minh nhất)
- ✅ Tự động retry khi lỗi
- ✅ Logging và monitoring
- ✅ Có thể tạo workflows phức tạp

---

## ❓ Câu Hỏi Thường Gặp

### Q1: API key có mất phí không?
**A:** KHÔNG! Gemini API key hoàn toàn miễn phí. Google cung cấp hạn mức sử dụng hàng ngày đủ cho nhu cầu cá nhân.

### Q2: API key có an toàn không?
**A:** API key được lưu trong session của bạn, KHÔNG lưu vào server. Mỗi lần mở web mới cần nhập lại.

### Q3: Tại sao AI không trả lời?
**A:** Kiểm tra:
- ✅ Đã nhập đúng API key chưa?
- ✅ API key còn hạn mức chưa?
- ✅ Kết nối internet ổn định chưa?

### Q4: Làm sao biết đang dùng Gemini hay Free AI?
**A:** Xem dòng trạng thái trong sidebar:
- **"Gemini Pro (Active)"** → Đang dùng Gemini
- **"Free AI (Offline)"** → Đang dùng Free AI

### Q5: n8n có bắt buộc không?
**A:** KHÔNG! n8n là optional. Web app hoạt động tốt với direct Gemini API.

### Q6: Tôi có thể dùng API key của người khác không?
**A:** KHÔNG nên! Mỗi người nên có API key riêng để:
- Bảo mật thông tin
- Tránh vượt hạn mức
- Theo dõi usage

---

## 🎉 Kết Luận

Bây giờ bạn đã biết cách:
1. ✅ Lấy Gemini API key miễn phí
2. ✅ Kích hoạt AI trên web app
3. ✅ Sử dụng các tính năng AI
4. ✅ Cấu hình n8n (nếu muốn)

**Chúc bạn sử dụng vui vẻ! 🔮✨**

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề, liên hệ:
- **Tác giả:** Vũ Việt Cường
- **Email:** [Thêm email nếu có]

---

*Cập nhật lần cuối: 2026-01-23*
