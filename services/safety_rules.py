from typing import Tuple, Dict


class SafetyRules:

    @staticmethod
    def assess(emotion: Dict) -> Tuple[int, str]:

        if not emotion:
            return 0, "No emotion data"

        label = emotion.get("label")
        secondary = emotion.get("secondary")
        confidence = emotion.get("confidence", 0.0)
        distribution = emotion.get("distribution", {}) or {}

        despair_score = distribution.get("despair", 0.0)
        sadness_score = distribution.get("sadness", 0.0)
        anger_score = distribution.get("anger", 0.0)

        #（高风险）

        # 强绝望主导
        if label == "despair" and despair_score >= 0.6:
            return 2, "High despair dominance"

        # despair概率高 + 高置信度
        if despair_score >= 0.5 and confidence >= 0.3:
            return 2, "Strong despair signal"

        # despair为次情绪但比例高
        if secondary == "despair" and despair_score >= 0.5:
            return 2, "Secondary despair but strong presence"

        # 中风险

        # sadness主导
        if label == "sadness" and sadness_score >= 0.4:
            return 1, "Sadness dominant"

        # anger主导
        if label == "anger" and anger_score >= 0.4:
            return 1, "Anger dominant"

        # despair较弱但存在
        if despair_score >= 0.3:
            return 1, "Moderate despair presence"

        # 低置信度负面（模糊但负面）
        if label in {"sadness", "anger"} and confidence < 0.2:
            return 1, "Low-confidence negative emotion"

        #默认低风险

        return 0, "Low risk"