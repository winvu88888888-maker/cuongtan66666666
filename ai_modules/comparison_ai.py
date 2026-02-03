"""
COMPARISON AI - So Sánh Nhiều Bàn/Quẻ
Phân tích và so sánh kết quả của nhiều lần xem
"""

from datetime import datetime


class ComparisonAI:
    """
    AI So sánh nhiều bàn/quẻ
    - So sánh kết quả giữa các lần xem
    - Tìm điểm chung và khác biệt
    - Đưa ra kết luận tổng hợp
    """
    
    def __init__(self):
        pass
    
    def compare_readings(self, readings):
        """
        So sánh nhiều lần xem quẻ
        
        Args:
            readings: List của các dict {chart_data, analysis, topic}
            
        Returns:
            Dict với phân tích so sánh
        """
        if not readings or len(readings) < 2:
            return {"error": "Cần ít nhất 2 lần xem để so sánh"}
        
        # Thu thập các metrics
        scores = []
        verdicts = []
        timings = []
        topics = []
        
        for r in readings:
            analysis = r.get("analysis", {})
            scores.append(analysis.get("xac_suat", {}).get("phan_tram", 0))
            verdicts.append(analysis.get("tuong_lai", {}).get("tom_tat", "N/A"))
            timings.append(analysis.get("thoi_gian", {}).get("days", "N/A"))
            topics.append(r.get("topic", "N/A"))
        
        # Phân tích
        avg_score = sum(scores) / len(scores)
        score_range = max(scores) - min(scores)
        
        # Tìm điểm chung
        common_verdict = max(set(verdicts), key=verdicts.count) if verdicts else "N/A"
        
        # Xác định xu hướng
        if scores[0] < scores[-1]:
            trend = "TĂNG - Các lần xem sau tốt hơn"
        elif scores[0] > scores[-1]:
            trend = "GIẢM - Các lần xem sau kém hơn"
        else:
            trend = "ỔN ĐỊNH - Kết quả nhất quán"
        
        # Đánh giá độ nhất quán
        if score_range <= 20:
            consistency = "CAO - Các kết quả khá đồng nhất"
        elif score_range <= 40:
            consistency = "TRUNG BÌNH - Có một số khác biệt"
        else:
            consistency = "THẤP - Kết quả khác nhau nhiều"
        
        return {
            "so_lan_xem": len(readings),
            "diem_trung_binh": round(avg_score, 1),
            "diem_cao_nhat": max(scores),
            "diem_thap_nhat": min(scores),
            "xu_huong": trend,
            "do_nhat_quan": consistency,
            "ket_luan_chung": common_verdict,
            "chi_tiet": self._generate_comparison_table(readings, scores, verdicts, timings)
        }
    
    def _generate_comparison_table(self, readings, scores, verdicts, timings):
        """Tạo bảng so sánh chi tiết"""
        table = []
        for i, r in enumerate(readings):
            table.append({
                "stt": i + 1,
                "topic": r.get("topic", "N/A"),
                "score": scores[i],
                "verdict": verdicts[i],
                "timing": timings[i]
            })
        return table
    
    def find_best_reading(self, readings):
        """Tìm lần xem tốt nhất"""
        if not readings:
            return None
        
        best = None
        best_score = -1
        
        for r in readings:
            score = r.get("analysis", {}).get("xac_suat", {}).get("phan_tram", 0)
            if score > best_score:
                best_score = score
                best = r
        
        return {
            "reading": best,
            "score": best_score,
            "recommendation": "Nên dựa theo kết quả của lần xem này"
        }
    
    def compare_same_topic(self, readings, topic):
        """So sánh các lần xem cùng chủ đề"""
        filtered = [r for r in readings if topic.lower() in r.get("topic", "").lower()]
        
        if len(filtered) < 2:
            return {"message": f"Chỉ có {len(filtered)} lần xem về chủ đề '{topic}'"}
        
        return self.compare_readings(filtered)
    
    def get_trend_analysis(self, readings, days=30):
        """Phân tích xu hướng theo thời gian"""
        # Giả sử readings đã có timestamp
        recent = []
        cutoff = datetime.now()
        
        for r in readings:
            try:
                ts = datetime.fromisoformat(r.get("timestamp", ""))
                diff = (cutoff - ts).days
                if diff <= days:
                    recent.append(r)
            except:
                pass
        
        if len(recent) < 2:
            return {"message": f"Không đủ dữ liệu trong {days} ngày gần đây"}
        
        # Sắp xếp theo thời gian
        recent.sort(key=lambda x: x.get("timestamp", ""))
        
        scores = [r.get("analysis", {}).get("xac_suat", {}).get("phan_tram", 0) for r in recent]
        
        # Tính trend
        if len(scores) >= 3:
            first_half = sum(scores[:len(scores)//2]) / (len(scores)//2)
            second_half = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
            
            if second_half > first_half + 10:
                trend = "📈 TÍCH CỰC - Vận may đang tăng"
            elif second_half < first_half - 10:
                trend = "📉 TIÊU CỰC - Vận may đang giảm"
            else:
                trend = "📊 ỔN ĐỊNH - Vận may không đổi"
        else:
            trend = "KHÔNG ĐỦ DỮ LIỆU"
        
        return {
            "period": f"{days} ngày",
            "readings_count": len(recent),
            "trend": trend,
            "average_score": round(sum(scores) / len(scores), 1)
        }
    
    def get_comparison_report(self, comparison_result):
        """Tạo báo cáo so sánh"""
        if "error" in comparison_result:
            return comparison_result["error"]
        
        output = []
        output.append("## 📊 BÁO CÁO SO SÁNH")
        output.append("")
        output.append(f"**Số lần xem:** {comparison_result['so_lan_xem']}")
        output.append(f"**Điểm trung bình:** {comparison_result['diem_trung_binh']}%")
        output.append(f"**Xu hướng:** {comparison_result['xu_huong']}")
        output.append(f"**Độ nhất quán:** {comparison_result['do_nhat_quan']}")
        output.append(f"**Kết luận chung:** {comparison_result['ket_luan_chung']}")
        output.append("")
        
        output.append("### Chi tiết từng lần xem:")
        output.append("| STT | Chủ đề | Điểm | Kết quả | Thời gian |")
        output.append("|-----|--------|------|---------|-----------|")
        
        for item in comparison_result.get("chi_tiet", []):
            output.append(f"| {item['stt']} | {item['topic'][:20]} | {item['score']}% | {item['verdict']} | {item['timing']} |")
        
        return "\n".join(output)


# Singleton
_comparison = None

def get_comparison_ai():
    global _comparison
    if _comparison is None:
        _comparison = ComparisonAI()
    return _comparison


if __name__ == "__main__":
    ai = get_comparison_ai()
    
    # Test comparison
    readings = [
        {"topic": "Xin việc A", "analysis": {"xac_suat": {"phan_tram": 70}, "tuong_lai": {"tom_tat": "CÁT"}, "thoi_gian": {"days": "3-7 ngày"}}},
        {"topic": "Xin việc B", "analysis": {"xac_suat": {"phan_tram": 85}, "tuong_lai": {"tom_tat": "CÁT"}, "thoi_gian": {"days": "1-2 tuần"}}},
        {"topic": "Xin việc C", "analysis": {"xac_suat": {"phan_tram": 60}, "tuong_lai": {"tom_tat": "BÌNH"}, "thoi_gian": {"days": "2-4 tuần"}}}
    ]
    
    result = ai.compare_readings(readings)
    print(ai.get_comparison_report(result))
