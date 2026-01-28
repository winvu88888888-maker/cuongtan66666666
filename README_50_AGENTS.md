# README: Hệ Thống 50 AI Agents + Web Search 24/7

## 🎯 Tính Năng Chính

### ✅ 50 AI Agents Tự Động
- Chạy **50 tasks mỗi chu kỳ** (thay vì 5)
- **15 workers đồng thời** để tối ưu tốc độ
- Tìm kiếm trên **Google + Internet** thực sự
- **Dual-phase search**: Web scraping + Gemini AI

### ✅ 100+ Chủ Đề Đa Dạng
- Kỳ Môn Độn Giáp, Kinh Dịch
- AI/Programming, Machine Learning
- Y Học, Phong Thủy
- Kinh Tế, Tài Chính
- Khoa Học, Văn Hóa
- ...và nhiều hơn nữa!

### ✅ Chạy 24/7 Tự Động
- **GitHub Actions**: Chạy mỗi 30 phút (48 lần/ngày)
- **Không cần mở web browser**
- Tự động commit & push dữ liệu mới
- Streamlit tự động cập nhật

### ✅ Tự Động Lưu API Key
- Paste API key **1 lần duy nhất**
- Hệ thống tự động lưu vào:
  - `custom_data.json`
  - `factory_config.json`
  - `.streamlit/secrets.toml`
- **Lần sau vào web = Chạy luôn!**

## 🚀 Cách Sử Dụng

### Lần Đầu Tiên
1. Vào web: https://cuongtan66666666.streamlit.app/
2. Paste Gemini API Key vào sidebar
3. ✅ Tick "Lưu khóa này vĩnh viễn"
4. Click "Kích hoạt ngay"
5. **XONG!** Hệ thống sẽ tự chạy 24/7

### Lần Sau
- Vào web → **Tự động chạy luôn!**
- Không cần nhập lại API key
- 50 agents đã chạy ngầm trên GitHub

## 📊 Kết Quả Mong Đợi

### Mỗi Ngày
- **2,400 tasks** (50 × 48 cycles)
- **~1,000-1,500 bản ghi** dữ liệu mới
- **~50-100 MB** dữ liệu thu thập

### Mỗi Tuần
- **16,800 tasks**
- **~5,000-10,000 bản ghi**
- **~500 MB - 1 GB** dữ liệu

### Mỗi Tháng
- **72,000 tasks**
- **~20,000-40,000 bản ghi**
- **~2-4 GB** dữ liệu (có nén)

## 🔧 Quản Lý

### Xem Trạng Thái
- Vào tab "🏭 Nhà Máy AI"
- Xem metrics:
  - Tổng chu kỳ đã chạy
  - Dữ liệu đã thu thập
  - Lần chạy cuối cùng

### Bật/Tắt 24/7
- Toggle "⚡ KÍCH HOẠT CHẾ ĐỘ TỰ TRỊ 24/7"
- Hệ thống sẽ tự động bật/tắt

### Chạy Thủ Công
- Click "🚀 CHẠY CHU KỲ THỦ CÔNG"
- 50 agents sẽ chạy ngay lập tức

## 📁 Cấu Trúc Dữ Liệu

```
data_hub/
├── hub_index.json          # Index tất cả dữ liệu
├── shard_0000.json         # Shard 1
├── shard_0001.json         # Shard 2
├── ...
└── factory_config.json     # Config 24/7
```

## ⚙️ Files Quan Trọng

- `ai_modules/web_searcher.py` - Tìm kiếm Google/Internet
- `ai_modules/autonomous_miner.py` - 50 AI agents
- `ai_modules/mining_strategist.py` - 100+ topics
- `.github/workflows/ai_mining_cron.yml` - GitHub Actions
- `web/ai_factory_tabs.py` - Dashboard UI

## 🔑 API Key Management

### Tự Động Lưu
Khi bạn paste API key vào web, hệ thống tự động lưu vào:
1. `custom_data.json` (từ web app)
2. `factory_config.json` (từ autonomous miner)
3. `.streamlit/secrets.toml` (nếu có)

### Tự Động Load
Khi chạy, hệ thống tự động tìm API key từ:
1. Session state (nếu đang mở web)
2. `factory_config.json`
3. `custom_data.json`
4. `.streamlit/secrets.toml`
5. Environment variable `GEMINI_API_KEY`

### GitHub Actions
- Thêm secret `GEMINI_API_KEY` trên GitHub
- Hoặc để hệ thống tự sync từ `custom_data.json`

## 🎉 Tóm Tắt

**Paste API key 1 lần → Chạy mãi mãi 24/7!**

- ✅ 50 AI agents
- ✅ Web search thực sự
- ✅ 100+ topics
- ✅ Tự động 24/7
- ✅ Không cần nhập lại key
- ✅ Tự động cập nhật web

**Hệ thống hoàn toàn tự động!** 🚀
