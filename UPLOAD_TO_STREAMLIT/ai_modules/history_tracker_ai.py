"""
HISTORY TRACKER AI - Lưu Trữ Lịch Sử Xem Quẻ
Theo dõi và phân tích lịch sử các lần xem quẻ
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Configuration
HISTORY_FILE = Path("data_hub/history_data.json")
MAX_HISTORY_ENTRIES = 1000


class HistoryTrackerAI:
    """
    AI Lưu trữ và phân tích lịch sử xem quẻ
    - Lưu mỗi lần xem quẻ
    - Phân tích xu hướng
    - So sánh kết quả thực tế
    """
    
    def __init__(self):
        self._ensure_history_file()
    
    def _ensure_history_file(self):
        """Đảm bảo file history tồn tại"""
        if not HISTORY_FILE.parent.exists():
            HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump({"entries": [], "stats": {}}, f)
    
    def save_reading(self, topic, chart_type, chart_data, prediction, notes=""):
        """
        Lưu một lần xem quẻ
        Args:
            topic: Chủ đề xem
            chart_type: Loại quẻ (QMDG, Mai Hoa, Lục Hào)
            chart_data: Dữ liệu bàn/quẻ
            prediction: Dự đoán AI đưa ra
            notes: Ghi chú thêm
        """
        entry = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "chart_type": chart_type,
            "chart_summary": self._summarize_chart(chart_data, chart_type),
            "prediction": prediction,
            "notes": notes,
            "actual_result": None,  # Sẽ cập nhật sau
            "verified": False
        }
        
        data = self._load_history()
        data["entries"].insert(0, entry)  # Newest first
        
        # Giới hạn số lượng
        if len(data["entries"]) > MAX_HISTORY_ENTRIES:
            data["entries"] = data["entries"][:MAX_HISTORY_ENTRIES]
        
        # Cập nhật thống kê
        data["stats"]["total_readings"] = len(data["entries"])
        data["stats"]["last_reading"] = entry["timestamp"]
        
        self._save_history(data)
        return entry["id"]
    
    def _summarize_chart(self, chart_data, chart_type):
        """Tóm tắt dữ liệu bàn/quẻ"""
        if chart_type == "QMDG":
            return {
                "gio": chart_data.get('gio', ''),
                "ngay": chart_data.get('ngay', ''),
                "cuc": chart_data.get('cuc', ''),
                "dich_ma": chart_data.get('dich_ma', '')
            }
        elif chart_type == "Mai Hoa":
            return {
                "ten_que": chart_data.get('ten', ''),
                "dong_hao": chart_data.get('dong_hao', 0),
                "bien_que": chart_data.get('ten_qua_bien', '')
            }
        elif chart_type == "Lục Hào":
            return {
                "ten_que": chart_data.get('ban', {}).get('name', ''),
                "dong_hao": chart_data.get('dong_hao', []),
                "cung": chart_data.get('ban', {}).get('palace', '')
            }
        return chart_data
    
    def update_actual_result(self, entry_id, actual_result, accuracy_score=None):
        """
        Cập nhật kết quả thực tế sau khi sự việc xảy ra
        Args:
            entry_id: ID của lần xem
            actual_result: Kết quả thực tế
            accuracy_score: Điểm chính xác (0-100)
        """
        data = self._load_history()
        
        for entry in data["entries"]:
            if entry["id"] == entry_id:
                entry["actual_result"] = actual_result
                entry["accuracy_score"] = accuracy_score
                entry["verified"] = True
                entry["verified_at"] = datetime.now().isoformat()
                break
        
        self._save_history(data)
        return True
    
    def get_history(self, limit=20, chart_type=None, topic_keyword=None):
        """Lấy lịch sử xem quẻ"""
        data = self._load_history()
        entries = data["entries"]
        
        # Filter theo loại quẻ
        if chart_type:
            entries = [e for e in entries if e["chart_type"] == chart_type]
        
        # Filter theo keyword
        if topic_keyword:
            keyword = topic_keyword.lower()
            entries = [e for e in entries if keyword in e["topic"].lower()]
        
        return entries[:limit]
    
    def get_similar_readings(self, topic, chart_type=None, limit=5):
        """Tìm các lần xem tương tự trước đó"""
        data = self._load_history()
        topic_words = set(topic.lower().split())
        
        similar = []
        for entry in data["entries"]:
            if chart_type and entry["chart_type"] != chart_type:
                continue
            
            entry_words = set(entry["topic"].lower().split())
            common = len(topic_words & entry_words)
            
            if common > 0:
                similar.append({
                    **entry,
                    "similarity": common / max(len(topic_words), len(entry_words))
                })
        
        # Sắp xếp theo độ tương tự
        similar.sort(key=lambda x: x["similarity"], reverse=True)
        return similar[:limit]
    
    def get_accuracy_stats(self):
        """Thống kê độ chính xác của các dự đoán"""
        data = self._load_history()
        verified = [e for e in data["entries"] if e.get("verified")]
        
        if not verified:
            return {"message": "Chưa có dữ liệu xác minh"}
        
        scores = [e.get("accuracy_score", 0) for e in verified if e.get("accuracy_score") is not None]
        
        return {
            "total_verified": len(verified),
            "total_readings": len(data["entries"]),
            "average_accuracy": round(sum(scores) / len(scores), 1) if scores else 0,
            "high_accuracy": len([s for s in scores if s >= 80]),
            "medium_accuracy": len([s for s in scores if 50 <= s < 80]),
            "low_accuracy": len([s for s in scores if s < 50])
        }
    
    def get_topic_trends(self):
        """Phân tích xu hướng chủ đề được xem nhiều"""
        data = self._load_history()
        
        topic_counts = {}
        for entry in data["entries"]:
            topic = entry["topic"].lower()
            # Tìm keywords chính
            for keyword in ["tiền", "việc", "tình", "sức khỏe", "nhà", "kiện", "thi"]:
                if keyword in topic:
                    topic_counts[keyword] = topic_counts.get(keyword, 0) + 1
        
        # Sắp xếp theo số lượng
        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "top_topics": sorted_topics[:10],
            "total_readings": len(data["entries"])
        }
    
    def _load_history(self):
        """Load history từ file"""
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"entries": [], "stats": {}}
    
    def _save_history(self, data):
        """Lưu history vào file"""
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_summary(self):
        """Lấy tóm tắt lịch sử"""
        data = self._load_history()
        stats = self.get_accuracy_stats()
        trends = self.get_topic_trends()
        
        output = []
        output.append("## 📚 LỊCH SỬ XEM QUẺ")
        output.append("")
        output.append(f"**Tổng số lần xem:** {len(data['entries'])}")
        output.append(f"**Đã xác minh:** {stats.get('total_verified', 0)}")
        output.append(f"**Độ chính xác TB:** {stats.get('average_accuracy', 'N/A')}%")
        output.append("")
        output.append("### Chủ đề phổ biến:")
        for topic, count in trends.get("top_topics", [])[:5]:
            output.append(f"- {topic.capitalize()}: {count} lần")
        
        return "\n".join(output)


# Singleton
_tracker = None

def get_history_tracker():
    global _tracker
    if _tracker is None:
        _tracker = HistoryTrackerAI()
    return _tracker


if __name__ == "__main__":
    tracker = get_history_tracker()
    
    # Test save
    tracker.save_reading(
        topic="Xin việc công ty ABC",
        chart_type="QMDG",
        chart_data={"gio": "Mão", "ngay": "Giáp Tý"},
        prediction="70% thành công, 2 tuần nữa có kết quả"
    )
    
    print(tracker.get_summary())
