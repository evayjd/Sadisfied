from typing import List, Dict, Optional,Tuple
from langdetect import detect
from snownlp import SnowNLP
from textblob import TextBlob, Blobber
from textblob_fr import PatternTagger, PatternAnalyzer
from langchain_core.messages import HumanMessage

# 情绪关键词词典（带权重）
DESPAIR_KEYWORDS = {

    "死": 0.9,
    "绝望": 0.7,
    "痛苦": 0.5,
    "活不下去": 1.0,
    "没有意义": 0.6,


    "suicide": 1.0,
    "kill myself": 1.0,
    "hopeless": 0.7,
    "worthless": 0.6,


    "envie de mourir": 1.0
}

ANGER_KEYWORDS = {
    "生气": 0.6,
    "愤怒": 0.8,
    "气死": 0.7,

    "angry": 0.6,
    "furious": 0.8,
    "rage": 0.7,

    "colère": 0.7,
    "furieux": 0.8
}

SADNESS_KEYWORDS = {
    "难过": 0.6,
    "伤心": 0.6,

    "sad": 0.5,
    "depressed": 0.8,

    "triste": 0.5,
    "déprimé": 0.8
}



# 法语情感分析器（单例）

tb_fr = Blobber(
    pos_tagger=PatternTagger(),
    analyzer=PatternAnalyzer()
)


# 情感分析函数


def detect_language(text: str) -> str:
    """检测文本语言"""
    try:
        return detect(text)
    except Exception:
        return "unknown"


def chinese_sentiment(text: str) -> float:
    """
    SnowNLP 返回 0~1
    统一映射为 -1~1
    """
    score = SnowNLP(text).sentiments
    return score * 2 - 1


def english_sentiment(text: str) -> float:
    """
    TextBlob polarity: -1~1
    """
    return TextBlob(text).sentiment.polarity


def french_sentiment(text: str) -> float:
    """
    textblob-fr polarity: -1~1
    """
    return tb_fr(text).sentiment[0]




class EmotionClassifier:

    @staticmethod
    def classify(messages: List) -> Dict:
        """
        1. 提取最后一条用户消息
        2. 语言识别
        3. 情感分析
        4. 关键词 + 情感分数证据融合
        5. 生成主情绪 / 次情绪 / 分布 / 置信度
        """

        text = EmotionClassifier._extract_last_user_message(messages)

        if not text:
            return EmotionClassifier._neutral()

        # ——语言识别
        lang = detect_language(text)

        # ——情感分数
        if lang == "zh":
            score = chinese_sentiment(text)
        elif lang == "fr":
            score = french_sentiment(text)
        else:
            score = english_sentiment(text)

        # pool
        # 每个情绪都是一个“可累加证据值”
        emotion_scores = {
            "positive": 0.0,
            "neutral": 0.0,
            "sadness": 0.0,
            "anger": 0.0,
            "despair": 0.0
        }

        # 关键词evidence
        EmotionClassifier._apply_keyword_scores(
            text=text,
            emotion_scores=emotion_scores
        )

        # 情感分数evidence
        EmotionClassifier._apply_sentiment_scores(
            score=score,
            emotion_scores=emotion_scores
        )

        # 归一化分布
        distribution = EmotionClassifier._normalize(emotion_scores)

        # 主情绪+次情绪
        primary, secondary = EmotionClassifier._select_primary_secondary(distribution)

        # 若出现强自杀关键词，确保 despair 不会被稀释掉
        if EmotionClassifier._has_strong_despair(text):
            if distribution["despair"] < 0.4:
                distribution["despair"] = 0.4
                distribution = EmotionClassifier._normalize(distribution)
                primary, secondary = EmotionClassifier._select_primary_secondary(distribution)

        #置信度
        confidence = EmotionClassifier._confidence_from_distribution(distribution)

        return EmotionClassifier._build(
            label=primary,
            secondary=secondary,
            confidence=confidence,
            reason=f"lang={lang}, sentiment_score={round(score, 3)}",
            distribution=distribution
        )

#——————辅助函数

    @staticmethod
    def _extract_last_user_message(messages: List) -> str:
        """提取最近一条 HumanMessage"""
        for m in reversed(messages):
            if isinstance(m, HumanMessage):
                return m.content.lower()
        return ""

    @staticmethod
    def _apply_keyword_scores(text: str, emotion_scores: Dict) -> None:
        """关键词 → 情绪证据加权"""
        for k, w in DESPAIR_KEYWORDS.items():
            if k in text:
                emotion_scores["despair"] += w

        for k, w in ANGER_KEYWORDS.items():
            if k in text:
                emotion_scores["anger"] += w

        for k, w in SADNESS_KEYWORDS.items():
            if k in text:
                emotion_scores["sadness"] += w

    @staticmethod
    def _apply_sentiment_scores(score: float, emotion_scores: Dict) -> None:
        """
        连续情感分数 → 多情绪证据
        """
        if score < 0:
            neg = abs(score)
            emotion_scores["sadness"] += neg * 0.6
            emotion_scores["anger"] += neg * 0.25
            emotion_scores["despair"] += neg * 0.15
        elif score > 0:
            emotion_scores["positive"] += score
        else:
            emotion_scores["neutral"] += 0.5

    @staticmethod
    def _normalize(scores: Dict) -> Dict:
        """将证据值归一化为概率分布"""
        total = sum(scores.values())
        if total <= 0:
            return {
                "positive": 0.0,
                "neutral": 1.0,
                "sadness": 0.0,
                "anger": 0.0,
                "despair": 0.0
            }
        return {
            k: round(v / total, 3)
            for k, v in scores.items()
        }

    @staticmethod
    def _select_primary_secondary(distribution: Dict) ->Tuple[str, Optional[str]]:
        """
        主情绪：概率最高
        次情绪：第二高，且与主情绪差距足够小
        """
        sorted_items = sorted(
            distribution.items(),
            key=lambda x: x[1],
            reverse=True
        )

        primary, primary_score = sorted_items[0]
        secondary, secondary_score = sorted_items[1]

        # 差距太大则不返回次情绪
        if primary_score - secondary_score > 0.25:
            return primary, None

        return primary, secondary

    @staticmethod
    def _confidence_from_distribution(distribution: Dict) -> float:
        """
        置信度定义：
        top1 - top2 的概率差
        """
        values = sorted(distribution.values(), reverse=True)
        if len(values) < 2:
            return 0.0
        return round(values[0] - values[1], 3)

    @staticmethod
    def _has_strong_despair(text: str) -> bool:
        """
        是否命中“强绝望 / 自杀”关键词
        """
        for k, w in DESPAIR_KEYWORDS.items():
            if w >= 0.9 and k in text:
                return True
        return False

    @staticmethod
    def _neutral() -> Dict:
        """无输入兜底"""
        return EmotionClassifier._build(
            label="neutral",
            secondary=None,
            confidence=0.9,
            reason="No user input",
            distribution={
                "positive": 0.0,
                "neutral": 1.0,
                "sadness": 0.0,
                "anger": 0.0,
                "despair": 0.0
            }
        )

    @staticmethod
    def _build(
        label: str,
        secondary: Optional[str],
        confidence: float,
        reason: str,
        distribution: Optional[Dict] = None
    ) -> Dict:
        """统一输出结构"""
        return {
            "label": label,
            "secondary": secondary,
            "confidence": confidence,
            "reason": reason,
            "distribution": distribution,
            
        }