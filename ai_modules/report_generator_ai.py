"""
REPORT GENERATOR AI - Xuất Báo Cáo Chi Tiết
Tạo báo cáo dạng text/markdown từ kết quả phân tích
"""

from datetime import datetime


class ReportGeneratorAI:
    """
    AI Tạo báo cáo chi tiết
    - Xuất báo cáo markdown
    - Format đẹp, dễ đọc
    - Tổng hợp nhiều nguồn dữ liệu
    """
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """Load các template báo cáo"""
        return {
            "qmdg": """# BÁO CÁO PHÂN TÍCH KỲ MÔN ĐỘN GIÁP

## Thông Tin Chung
{info_section}

## Phân Tích Bàn QMDG
{analysis_section}

## Dự Đoán Chi Tiết
{prediction_section}

## Lời Khuyên
{advice_section}

---
*Báo cáo được tạo tự động bởi QMDG AI System*
*Thời gian: {timestamp}*
""",
            "mai_hoa": """# BÁO CÁO PHÂN TÍCH MAI HOA DỊCH SỐ

## Thông Tin Quẻ
{quai_info}

## Thể/Dụng Quan Hệ
{the_dung_section}

## Dự Đoán
{prediction_section}

## Kết Luận
{conclusion_section}

---
*Thời gian: {timestamp}*
""",
            "luc_hao": """# BÁO CÁO PHÂN TÍCH LỤC HÀO

## Thông Tin Quẻ
{quai_info}

## Dụng Thần
{dung_than_section}

## Hào Động
{hao_dong_section}

## Kết Quả
{result_section}

---
*Thời gian: {timestamp}*
"""
        }
    
    def generate_qmdg_report(self, chart_data, analysis, topic):
        """Tạo báo cáo QMDG"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Info section
        info_lines = [
            f"- **Chủ đề:** {topic}",
            f"- **Thời gian lập bàn:** {chart_data.get('datetime', 'N/A')}",
            f"- **Cục số:** {chart_data.get('cuc', 'N/A')}",
            f"- **Độn (Âm/Dương):** {chart_data.get('don_type', 'N/A')}"
        ]
        
        # Analysis section
        analysis_lines = []
        if analysis.get("chi_tiet"):
            for key, value in analysis["chi_tiet"].items():
                analysis_lines.append(f"### {key}")
                if isinstance(value, list):
                    for item in value:
                        analysis_lines.append(f"- {item}")
                else:
                    analysis_lines.append(f"{value}")
        
        # Prediction section
        pred = analysis.get("tuong_lai", {})
        pred_lines = [
            f"### Kết quả dự đoán: **{pred.get('tom_tat', 'N/A')}**",
            "",
            "#### Chi tiết:"
        ]
        for detail in pred.get("chi_tiet", []):
            pred_lines.append(f"- {detail}")
        
        # Timing
        timing = analysis.get("thoi_gian", {})
        pred_lines.extend([
            "",
            "#### Thời gian:",
            f"- Tốc độ: {timing.get('speed', 'N/A')}",
            f"- Khoảng: {timing.get('days', 'N/A')}",
            f"- Ngày ứng kỳ: {timing.get('ngay_ung', 'N/A')}"
        ])
        
        # Probability
        prob = analysis.get("xac_suat", {})
        pred_lines.extend([
            "",
            "#### Xác suất:",
            f"- **{prob.get('phan_tram', 0)}%** - {prob.get('danh_gia', 'N/A')}"
        ])
        
        # Advice section
        advice = analysis.get("tuong_lai", {}).get("khuyen_nghi", [])
        advice_lines = []
        for a in advice:
            advice_lines.append(f"- {a}")
        
        # Fill template
        report = self.templates["qmdg"].format(
            info_section="\n".join(info_lines),
            analysis_section="\n".join(analysis_lines),
            prediction_section="\n".join(pred_lines),
            advice_section="\n".join(advice_lines) or "- Không có lời khuyên đặc biệt",
            timestamp=timestamp
        )
        
        return report
    
    def generate_mai_hoa_report(self, mai_hoa_data, analysis, topic):
        """Tạo báo cáo Mai Hoa"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Quai info
        quai_lines = [
            f"- **Tên quẻ:** {mai_hoa_data.get('ten', 'N/A')}",
            f"- **Thượng quái:** {mai_hoa_data.get('upper', 'N/A')}",
            f"- **Hạ quái:** {mai_hoa_data.get('lower', 'N/A')}",
            f"- **Hào động:** {mai_hoa_data.get('dong_hao', 'N/A')}",
            f"- **Quẻ biến:** {mai_hoa_data.get('ten_qua_bien', 'N/A')}"
        ]
        
        # The/Dung
        the_dung = analysis.get("the_dung", {})
        the_dung_lines = [
            f"### Thể quái: {the_dung.get('the', {}).get('ten', 'N/A')} ({the_dung.get('the', {}).get('hanh', '')})",
            f"- Tượng: {the_dung.get('the', {}).get('tuong', '')}",
            "",
            f"### Dụng quái: {the_dung.get('dung', {}).get('ten', 'N/A')} ({the_dung.get('dung', {}).get('hanh', '')})",
            f"- Tượng: {the_dung.get('dung', {}).get('tuong', '')}",
            "",
            f"### Quan hệ: **{analysis.get('quan_he', {}).get('verdict', 'N/A')}**",
            f"{analysis.get('quan_he', {}).get('giai_thich', '')}"
        ]
        
        # Prediction
        timing = analysis.get("thoi_gian", {})
        qty = analysis.get("so_luong", {})
        pred_lines = [
            f"### Thời gian: {timing.get('mo_ta', 'N/A')}",
            f"### Số lượng: {qty.get('mo_ta', 'N/A')}"
        ]
        
        # Conclusion
        ket_luan = analysis.get("ket_luan", {})
        conclusion_lines = [
            f"## Điểm: **{ket_luan.get('diem', 0)}/100** - {ket_luan.get('verdict', 'N/A')}",
            f"",
            f"**{ket_luan.get('loi_khuyen', '')}**",
            "",
            "### Chi tiết:"
        ]
        for detail in ket_luan.get("chi_tiet", []):
            conclusion_lines.append(detail)
        
        report = self.templates["mai_hoa"].format(
            quai_info="\n".join(quai_lines),
            the_dung_section="\n".join(the_dung_lines),
            prediction_section="\n".join(pred_lines),
            conclusion_section="\n".join(conclusion_lines),
            timestamp=timestamp
        )
        
        return report
    
    def generate_luc_hao_report(self, luc_hao_data, analysis, topic):
        """Tạo báo cáo Lục Hào"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Quai info
        ban = luc_hao_data.get("ban", {})
        quai_lines = [
            f"- **Tên quẻ:** {ban.get('name', 'N/A')}",
            f"- **Cung:** {ban.get('palace', 'N/A')}",
            f"- **Thế/Ứng:** {luc_hao_data.get('the_ung', 'N/A')}"
        ]
        
        # Dung Than
        dung_than = analysis.get("dung_than", {})
        dung_status = analysis.get("dung_than_status", {})
        dung_lines = [
            f"### {dung_than.get('ten', 'N/A')}",
            f"- Tượng: {dung_than.get('tuong', '')}",
            f"- Lý do: {dung_than.get('ly_do', '')}",
            f"- Trạng thái: {dung_status.get('mo_ta', '')}"
        ]
        
        # Hao dong
        dong_hao = analysis.get("dong_hao", {})
        hao_lines = [
            f"- **Số hào động:** {dong_hao.get('so_luong', 0)}",
            f"- {dong_hao.get('y_nghia', '')}"
        ]
        if dong_hao.get("mo_ta"):
            hao_lines.append(f"- {dong_hao.get('mo_ta')}")
        
        # Result
        ket_luan = analysis.get("ket_luan", {})
        timing = analysis.get("thoi_gian", {})
        result_lines = [
            f"## Điểm: **{ket_luan.get('diem', 0)}/100** - {ket_luan.get('verdict', 'N/A')}",
            "",
            f"**{ket_luan.get('loi_khuyen', '')}**",
            "",
            f"### Thời gian: {timing.get('mo_ta', 'N/A')}",
            f"### Khoảng: **{timing.get('khoang', 'N/A')}**"
        ]
        
        report = self.templates["luc_hao"].format(
            quai_info="\n".join(quai_lines),
            dung_than_section="\n".join(dung_lines),
            hao_dong_section="\n".join(hao_lines),
            result_section="\n".join(result_lines),
            timestamp=timestamp
        )
        
        return report
    
    def generate_comparison_report(self, readings):
        """Tạo báo cáo so sánh nhiều lần xem"""
        output = ["# BÁO CÁO SO SÁNH", ""]
        
        output.append(f"**Số lần xem:** {len(readings)}")
        output.append("")
        
        output.append("| STT | Thời gian | Chủ đề | Kết quả | Xác suất |")
        output.append("|-----|-----------|--------|---------|----------|")
        
        for i, reading in enumerate(readings, 1):
            output.append(f"| {i} | {reading.get('timestamp', 'N/A')[:10]} | {reading.get('topic', 'N/A')[:20]} | {reading.get('verdict', 'N/A')} | {reading.get('score', 'N/A')}% |")
        
        return "\n".join(output)
    
    def save_report(self, report, filename, folder="reports"):
        """Lưu báo cáo ra file"""
        from pathlib import Path
        
        report_dir = Path(folder)
        report_dir.mkdir(exist_ok=True)
        
        filepath = report_dir / f"{filename}.md"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return str(filepath)


# Singleton
_generator = None

def get_report_generator():
    global _generator
    if _generator is None:
        _generator = ReportGeneratorAI()
    return _generator


if __name__ == "__main__":
    generator = get_report_generator()
    
    # Test QMDG report
    chart = {"datetime": "2024-02-01 15:00", "cuc": "5", "don_type": "Dương Độn"}
    analysis = {
        "tuong_lai": {"tom_tat": "CÁT", "chi_tiet": ["Việc sẽ thành"], "khuyen_nghi": ["Tiến hành ngay"]},
        "thoi_gian": {"speed": "nhanh", "days": "3-7 ngày", "ngay_ung": "2024-02-08"},
        "xac_suat": {"phan_tram": 75, "danh_gia": "Tốt"}
    }
    
    print(generator.generate_qmdg_report(chart, analysis, "Xin việc"))
