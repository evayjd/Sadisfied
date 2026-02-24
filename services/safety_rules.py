class SafetyRules:

    @staticmethod
    def assess(emotion: dict) -> tuple[int, str]:#第一个int是风险等级，第二个str是风险原因
        """
        input emotion dict
        output (risk_level, risk_reason)
        """

        # 先占位
        return 0, "PLACEHOLDER"
    
    #之后risklevel可以改为enum？
    #emotion dict的格式也可以再商量，先这样简单一点，后续可以根据需要调整