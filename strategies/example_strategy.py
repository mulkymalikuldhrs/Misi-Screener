# strategies/example_strategy.py

"""
This is an example of a simple trading strategy that can be selected and
executed by the TraderAgent.

Each strategy should be a class with a clear `execute` method.
"""

class RsiMeanReversion:
    def __init__(self, rsi_period=14, overbought_threshold=70, oversold_threshold=30):
        self.rsi_period = rsi_period
        self.overbought_threshold = overbought_threshold
        self.oversold_threshold = oversold_threshold

    def execute(self, technical_analysis_report):
        """
        Analyzes the technical report to see if this strategy's conditions are met.

        Args:
            technical_analysis_report: The report from the TechnicalAnalystAgent.

        Returns:
            A signal ("BUY", "SELL", or None) if the conditions are met.
        """
        rsi_value = technical_analysis_report.get('rsi', 50) # Default to neutral

        if rsi_value < self.oversold_threshold:
            return "BUY"
        elif rsi_value > self.overbought_threshold:
            return "SELL"
        else:
            return None
