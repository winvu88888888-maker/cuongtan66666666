# -*- coding: utf-8 -*-
import os
import zipfile
import json
from datetime import datetime

class PackagerAI:
    def __init__(self, output_dir="dist"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def package_project(self, project_path, project_name):
        """Đóng gói toàn bộ thư mục project thành file ZIP"""
        zip_name = f"{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join(self.output_dir, zip_name)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(project_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, project_path)
                    zipf.write(file_path, arcname)
        
        return zip_path

    def generate_final_report(self, analysis_data, test_results, qmdg_data):
        """Tạo báo cáo kết quả cuối cùng bằng Markdown"""
        report = f"""# BÁO CÁO KẾT QUẢ PHÁT TRIỂN PHẦN MỀM AI
        
## 1. Thông tin dự án
- Thời gian hoàn thành: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Trạng thái QMDG: {'THUẬN LỢI' if qmdg_data.get('favorable') else 'CẦN LƯU Ý'}

## 2. Phân tích Kỳ Môn Độn Giáp (Đường đi đúng)
{qmdg_data.get('path_advice', 'N/A')}

## 3. Chỉ số Code (Code Analyzer)
- Tổng số dòng: {analysis_data['metrics']['total_lines']}
- Số hàm: {analysis_data['metrics']['functions']}
- Điểm chất lượng AI: {analysis_data.get('quality_score', 'N/A')}/100

## 4. Kết quả Kiểm thử (Tester AI)
- Trạng thái: {'THÀNH CÔNG' if test_results.get('success') else 'THẤT BẠI'}
- Chi tiết: {test_results.get('output', 'Không có dữ liệu')}

---
*Báo cáo được tạo tự động bởi AI Factory Orchestrator*
"""
        report_path = os.path.join(self.output_dir, "FINAL_REPORT.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        return report_path