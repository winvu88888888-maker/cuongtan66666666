"""
PREDICTION VALIDATOR AI - Xác Minh Dự Đoán
Theo dõi và đánh giá độ chính xác của các dự đoán
"""

import json
from datetime import datetime, timedelta
from pathlib import Path


class PredictionValidatorAI:
    """
    AI Xác minh độ chính xác của dự đoán
    - So sánh dự đoán với thực tế
    - Tính điểm chính xác
    - Phân tích patterns thành công/thất bại
    """
    
    def __init__(self):
        self.validation_rules = self._load_rules()
    
    def _load_rules(self):
        """Load các quy tắc đánh giá"""
        return {
            "time_tolerance": 7,  # Sai số thời gian (ngày)
            "quantity_tolerance": 0.2,  # Sai số số lượng (20%)
            "score_weights": {
                "outcome": 50,      # Kết quả đúng/sai: 50%
                "timing": 25,       # Thời gian: 25%
                "quantity": 15,     # Số lượng: 15%
                "details": 10       # Chi tiết: 10%
            }
        }
    
    def validate_prediction(self, prediction, actual_result):
        """
        Xác minh một dự đoán với kết quả thực tế
        
        Args:
            prediction: Dict chứa dự đoán {outcome, timing, quantity, details}
            actual_result: Dict chứa kết quả thực {outcome, timing, quantity, details}
            
        Returns:
            Dict với điểm số và phân tích chi tiết
        """
        scores = {}
        details = []
        
        # 1. Đánh giá kết quả (tốt/xấu/thành/bại)
        pred_outcome = prediction.get("outcome", "").lower()
        actual_outcome = actual_result.get("outcome", "").lower()
        
        outcome_match = self._compare_outcomes(pred_outcome, actual_outcome)
        scores["outcome"] = outcome_match * self.validation_rules["score_weights"]["outcome"]
        details.append(f"Kết quả: {'Đúng' if outcome_match >= 0.8 else 'Sai'} ({int(outcome_match*100)}%)")
        
        # 2. Đánh giá thời gian
        pred_timing = prediction.get("timing")
        actual_timing = actual_result.get("timing")
        
        if pred_timing and actual_timing:
            timing_match = self._compare_timing(pred_timing, actual_timing)
            scores["timing"] = timing_match * self.validation_rules["score_weights"]["timing"]
            details.append(f"Thời gian: {'Chính xác' if timing_match >= 0.8 else 'Sai lệch'} ({int(timing_match*100)}%)")
        else:
            scores["timing"] = 0
            details.append("Thời gian: Không có dữ liệu")
        
        # 3. Đánh giá số lượng
        pred_qty = prediction.get("quantity")
        actual_qty = actual_result.get("quantity")
        
        if pred_qty is not None and actual_qty is not None:
            qty_match = self._compare_quantity(pred_qty, actual_qty)
            scores["quantity"] = qty_match * self.validation_rules["score_weights"]["quantity"]
            details.append(f"Số lượng: {'Đúng' if qty_match >= 0.8 else 'Sai'} (dự đoán {pred_qty}, thực tế {actual_qty})")
        else:
            scores["quantity"] = 0
            details.append("Số lượng: Không áp dụng")
        
        # 4. Đánh giá chi tiết
        pred_details = prediction.get("details", [])
        actual_details = actual_result.get("details", [])
        
        if pred_details and actual_details:
            detail_match = self._compare_details(pred_details, actual_details)
            scores["details"] = detail_match * self.validation_rules["score_weights"]["details"]
        else:
            scores["details"] = self.validation_rules["score_weights"]["details"] * 0.5
        
        # Tổng điểm
        total_score = sum(scores.values())
        
        return {
            "total_score": round(total_score),
            "breakdown": scores,
            "details": details,
            "verdict": self._score_to_verdict(total_score),
            "validated_at": datetime.now().isoformat()
        }
    
    def _compare_outcomes(self, pred, actual):
        """So sánh kết quả định tính"""
        positive_words = ["tốt", "thành", "cát", "được", "có", "thuận", "thắng"]
        negative_words = ["xấu", "bại", "hung", "không", "mất", "khó", "thua"]
        
        pred_positive = any(w in pred for w in positive_words)
        pred_negative = any(w in pred for w in negative_words)
        
        actual_positive = any(w in actual for w in positive_words)
        actual_negative = any(w in actual for w in negative_words)
        
        if pred_positive == actual_positive and pred_negative == actual_negative:
            return 1.0
        elif pred_positive == actual_positive or pred_negative == actual_negative:
            return 0.5
        else:
            return 0.0
    
    def _compare_timing(self, pred_timing, actual_timing):
        """So sánh thời gian"""
        try:
            # Parse dates
            if isinstance(pred_timing, str):
                pred_date = datetime.fromisoformat(pred_timing)
            else:
                pred_date = pred_timing
            
            if isinstance(actual_timing, str):
                actual_date = datetime.fromisoformat(actual_timing)
            else:
                actual_date = actual_timing
            
            # Tính sai số (ngày)
            diff = abs((pred_date - actual_date).days)
            tolerance = self.validation_rules["time_tolerance"]
            
            if diff <= tolerance:
                return 1.0 - (diff / tolerance) * 0.5
            else:
                return max(0, 1.0 - (diff / tolerance))
        except:
            return 0.5  # Không so sánh được
    
    def _compare_quantity(self, pred_qty, actual_qty):
        """So sánh số lượng"""
        try:
            pred = float(pred_qty)
            actual = float(actual_qty)
            
            if actual == 0:
                return 1.0 if pred == 0 else 0.0
            
            diff_ratio = abs(pred - actual) / actual
            tolerance = self.validation_rules["quantity_tolerance"]
            
            if diff_ratio <= tolerance:
                return 1.0
            else:
                return max(0, 1.0 - (diff_ratio - tolerance))
        except:
            return 0.5
    
    def _compare_details(self, pred_details, actual_details):
        """So sánh chi tiết"""
        if not pred_details or not actual_details:
            return 0.5
        
        pred_set = set(str(d).lower() for d in pred_details)
        actual_set = set(str(d).lower() for d in actual_details)
        
        intersection = len(pred_set & actual_set)
        union = len(pred_set | actual_set)
        
        return intersection / union if union > 0 else 0.5
    
    def _score_to_verdict(self, score):
        """Chuyển điểm thành đánh giá"""
        if score >= 90:
            return "XUẤT SẮC - Dự đoán cực kỳ chính xác"
        elif score >= 75:
            return "TỐT - Dự đoán chính xác cao"
        elif score >= 60:
            return "KHÁ - Dự đoán đúng phần lớn"
        elif score >= 40:
            return "TRUNG BÌNH - Dự đoán đúng một phần"
        else:
            return "CẦN CẢI THIỆN - Dự đoán chưa chính xác"
    
    def analyze_pattern(self, validations):
        """
        Phân tích patterns từ nhiều lần xác minh
        
        Args:
            validations: List các lần xác minh
            
        Returns:
            Dict phân tích patterns
        """
        if not validations:
            return {"message": "Chưa có dữ liệu"}
        
        scores = [v.get("total_score", 0) for v in validations]
        
        # Tìm patterns
        high_accuracy = [v for v in validations if v.get("total_score", 0) >= 75]
        low_accuracy = [v for v in validations if v.get("total_score", 0) < 50]
        
        return {
            "total_validations": len(validations),
            "average_score": round(sum(scores) / len(scores), 1),
            "high_accuracy_count": len(high_accuracy),
            "low_accuracy_count": len(low_accuracy),
            "accuracy_rate": round(len(high_accuracy) / len(validations) * 100, 1),
            "recommendation": self._generate_recommendation(scores)
        }
    
    def _generate_recommendation(self, scores):
        """Tạo khuyến nghị cải thiện"""
        avg = sum(scores) / len(scores) if scores else 0
        
        if avg >= 75:
            return "Dự đoán đang hoạt động tốt. Tiếp tục phương pháp hiện tại."
        elif avg >= 50:
            return "Cần cải thiện độ chính xác về thời gian và số lượng."
        else:
            return "Nên xem xét lại phương pháp luận giải và tham khảo thêm case study."
    
    def get_validation_report(self, validation_result):
        """Tạo báo cáo xác minh"""
        output = []
        output.append("## ✅ BÁO CÁO XÁC MINH DỰ ĐOÁN")
        output.append("")
        output.append(f"### Điểm tổng: **{validation_result['total_score']}/100**")
        output.append(f"**{validation_result['verdict']}**")
        output.append("")
        output.append("### Chi tiết:")
        for detail in validation_result["details"]:
            output.append(f"- {detail}")
        output.append("")
        output.append("### Điểm thành phần:")
        for key, score in validation_result["breakdown"].items():
            output.append(f"- {key.capitalize()}: {round(score, 1)}")
        
        return "\n".join(output)


# Singleton
_validator = None

def get_prediction_validator():
    global _validator
    if _validator is None:
        _validator = PredictionValidatorAI()
    return _validator


if __name__ == "__main__":
    validator = get_prediction_validator()
    
    # Test validation
    prediction = {
        "outcome": "Công việc sẽ thành công tốt đẹp",
        "timing": "2024-02-15",
        "quantity": 10,
        "details": ["thăng tiến", "tăng lương", "được khen"]
    }
    
    actual = {
        "outcome": "Đã được nhận việc thành công",
        "timing": "2024-02-20",
        "quantity": 12,
        "details": ["được nhận", "lương cao", "môi trường tốt"]
    }
    
    result = validator.validate_prediction(prediction, actual)
    print(validator.get_validation_report(result))
