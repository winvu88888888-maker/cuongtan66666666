# 🌐 Kích Hoạt Chạy Trên Cloud (Không Nặng Máy)

## ✅ Giải Pháp: GitHub Actions

**GitHub Actions = Chạy trên cloud GitHub (MIỄN PHÍ)**
- ✅ Không tốn tài nguyên máy bạn
- ✅ Chạy 24/7 tự động
- ✅ Mỗi 30 phút chạy 1 lần

## 🚀 Cách Kích Hoạt

### Bước 1: Kiểm Tra GitHub Actions

1. Vào: https://github.com/winvu88888888-maker/cuongtan66666666/actions
2. Xem workflow **"AI Factory 24/7 Independent Mining"**
3. Kiểm tra:
   - ✅ Có workflow này không?
   - ✅ Workflow có bật không? (nếu tắt, click "Enable workflow")

### Bước 2: Thêm API Key Secret (Quan trọng!)

1. Vào: https://github.com/winvu88888888-maker/cuongtan66666666/settings/secrets/actions
2. Click **"New repository secret"**
3. Điền:
   - Name: `GEMINI_API_KEY`
   - Value: `AIzaSyDv_tCfjrTOXSNQhtKSneaFlyrM7RVp9Ow`
4. Click **"Add secret"**

### Bước 3: Chạy Thử Ngay (Không Đợi 30 Phút)

1. Vào: https://github.com/winvu88888888-maker/cuongtan66666666/actions
2. Click workflow **"AI Factory 24/7 Independent Mining"**
3. Click **"Run workflow"** (nút bên phải)
4. Click **"Run workflow"** (xác nhận)
5. Đợi 2-5 phút → Xem kết quả

## 📊 Xác Nhận Đang Chạy

### Sau Khi Chạy Workflow:

1. **Màu xanh** ✅ = Thành công
2. **Màu đỏ** ❌ = Có lỗi (click vào xem logs)

### Kiểm Tra Dữ Liệu:

1. Vào: https://github.com/winvu88888888-maker/cuongtan66666666/blob/main/data_hub/factory_config.json
2. Xem `"total_cycles"` - sẽ tăng dần (2 → 3 → 4...)
3. Xem `"last_run"` - cập nhật mỗi 30 phút

## 🎯 Kết Quả

**Sau khi setup xong:**
- ✅ GitHub Actions tự chạy mỗi 30 phút
- ✅ 50 AI agents chạy trên cloud GitHub
- ✅ Máy bạn không tốn tài nguyên
- ✅ Tắt máy vẫn chạy
- ✅ Hoàn toàn miễn phí

**Về Streamlit Web:**
- Web có thể cần config riêng
- Nhưng dữ liệu sẽ tự động lưu vào GitHub
- Bạn có thể xem dữ liệu trực tiếp trên GitHub

## 🔑 Tóm Tắt 3 Bước

1. **Enable workflow** trên GitHub Actions
2. **Add API key secret**: `GEMINI_API_KEY`
3. **Run workflow** thủ công 1 lần để test

**Xong! Hệ thống sẽ tự chạy 24/7 trên cloud!** 🚀
