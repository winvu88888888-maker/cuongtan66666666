# 🚀 SCRIPT TỰ ĐỘNG - HƯỚNG DẪN SỬ DỤNG

## ✨ MỤC ĐÍCH

Script `FIX_AND_DEPLOY_ALL.bat` sẽ tự động làm **TẤT CẢ** cho bạn:

✅ Kiểm tra Git status  
✅ Add tất cả files (kể cả untracked)  
✅ Commit với message chi tiết  
✅ Pull latest changes  
✅ Push lên GitHub  
✅ Tùy chọn mở web apps tự động  

---

## 🎯 CÁCH DÙNG

### Cách 1: Double-Click (Đơn Giản Nhất)

1. Mở **File Explorer**
2. Vào: `C:\Users\GHC\Desktop\python1 - Copy\UPLOAD_TO_STREAMLIT`
3. **Double-click** vào file: `FIX_AND_DEPLOY_ALL.bat`
4. Chờ script chạy xong
5. Khi hỏi "Bạn có muốn mở web app?", nhấn `Y` hoặc `N`

### Cách 2: Chạy Từ Terminal

```cmd
cd "C:\Users\GHC\Desktop\python1 - Copy\UPLOAD_TO_STREAMLIT"
FIX_AND_DEPLOY_ALL.bat
```

---

## 📋 SCRIPT SẼ LÀM GÌ?

### Bước 1: Git Status
Kiểm tra files nào đã thay đổi

### Bước 2: Add All Files
```bash
git add -A
```
Thêm TẤT CẢ files, kể cả:
- Modified files
- Untracked files
- Deleted files

### Bước 3: Check Changes
Hiển thị files sẽ được commit

### Bước 4: Commit
```bash
git commit -m "🔥 MEGA FIX: ..."
```
Commit với message chi tiết về tất cả fixes

### Bước 5: Pull Latest
```bash
git pull --rebase origin main
```
Lấy code mới nhất từ GitHub và merge

### Bước 6: Push
```bash
git push origin main
```
Đẩy tất cả lên GitHub

### Bước 7 (Optional): Mở Web Apps
Nếu bạn chọn `Y`, script sẽ tự động mở:
- https://cuongtan888888.streamlit.app/
- https://cuongtan66666666.streamlit.app/

---

## ✅ SAU KHI CHẠY SCRIPT

### 1. Chờ Deploy (1-2 phút)

Streamlit Cloud sẽ tự động:
- Phát hiện code mới
- Rebuild app
- Deploy lên production

### 2. Kiểm Tra Web App

1. Nếu script chưa tự mở, vào:
   - https://cuongtan888888.streamlit.app/

2. Nhấn **Ctrl+Shift+R** (hard refresh)

3. Xem sidebar → "🤖 Cấu hình AI"

### 3. Xác Nhận LED Hoạt Động

| Trạng Thái | Ý Nghĩa |
|------------|---------|
| 🟢 Xanh - "HOẠT ĐỘNG TỐT" | API OK, app đang chạy bình thường |
| 🔴 Đỏ - "LỖI KẾT NỐI" | API lỗi, cần tạo key mới |
| 🟡 Vàng - "CHƯA KIỂM TRA" | Chưa check, click "Kiểm tra kết nối ngay" |

### 4. Nếu Vẫn Thấy LED Đỏ

**Nguyên nhân:** API Key hết quota

**Giải pháp:**
1. Vào: https://aistudio.google.com/app/apikey
2. Tạo API Key mới
3. Paste vào ô "Thay đổi API Key"
4. Check ✅ "Lưu khóa này vĩnh viễn"
5. Click "CẬP NHẬT KEY MỚI"

---

## 🐛 TROUBLESHOOTING

### Lỗi 1: "fatal: not a git repository"

**Nguyên nhân:** Chạy sai folder

**Giải pháp:** Chắc chắn bạn đang ở:
```
C:\Users\GHC\Desktop\python1 - Copy\UPLOAD_TO_STREAMLIT
```

### Lỗi 2: "error: failed to push"

**Nguyên nhân:** Có conflict hoặc connection issue

**Giải pháp:**
```cmd
git pull --rebase origin main
git push origin main --force
```

### Lỗi 3: "Permission denied"

**Nguyên nhân:** Chưa đăng nhập Git

**Giải pháp:**
```cmd
git config user.name "winvu88888888-maker"
git config user.email "winvu88888888@gmail.com"
```

### Lỗi 4: Script Không Commit Gì

**Nguyên nhân:** Không có thay đổi hoặc file chưa save

**Giải pháp:**
1. Mở VS Code
2. Save tất cả files (Ctrl+K, S)
3. Chạy lại script

---

## 📊 OUTPUT MẪU

```
====================================================
  SCRIPT TỰ ĐỘNG - FIX VÀ DEPLOY HẾT MỌI THỨ
====================================================

[Bước 1/6] Kiểm tra Git status...
On branch main
Changes not staged for commit:
  modified:   app.py
  modified:   gemini_helper.py

[Bước 2/6] Adding TẤT CẢ files...

[Bước 3/6] Checking changes...
Changes to be committed:
  modified:   app.py
  modified:   gemini_helper.py
  new file:   FIX_AND_DEPLOY_ALL.bat

[Bước 4/6] Committing...
[main abc123] 🔥 MEGA FIX: ...
 3 files changed, 89 insertions(+), 24 deletions(-)

[Bước 5/6] Pulling latest...
Already up to date.

[Bước 6/6] Pushing to GitHub...
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
...
To https://github.com/winvu88888888-maker/cuongtan66666666.git
   def456..ghi789  main -> main

====================================================
             HOÀN TẤT!
====================================================

✅ Tất cả thay đổi đã được commit
✅ Đã push lên GitHub thành công
✅ Streamlit Cloud sẽ tự động deploy trong 1-2 phút

🌐 Web Apps: https://cuongtan888888.streamlit.app/
⏰ Chờ 1-2 phút, sau đó Ctrl+F5!
```

---

## 💡 TIPS

1. **Luôn check LED** sau khi deploy để biết API có OK không

2. **Dùng Flash model** để tiết kiệm quota (script đã config tự động)

3. **Tạo nhiều API keys** để backup khi hết quota

4. **Bookmark script** này để dùng thường xuyên khi có changes

---

## 🎉 KẾT LUẬN

Script này là **giải pháp 1-click** cho mọi vấn đề:
- ✅ Không cần nhớ git commands
- ✅ Không cần check từng bước
- ✅ Tự động mở web app
- ✅ Chi tiết, dễ debug

**Chỉ cần double-click và chờ!** 🚀

---

**Tác giả:** AI Assistant  
**Ngày tạo:** 2026-02-02  
**Version:** 1.0.0
