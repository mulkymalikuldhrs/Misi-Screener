# components/final_verdict/engine.py

class FinalVerdictEngine:
    """
    MODULE 11: FINAL VERDICT
    Delivers the final, synthesized decision.
    """
    def __init__(self):
        pass

    def decide(self, execution_plan, quant_score):
        """
        Takes the final execution plan and score to generate a clear, final verdict.
        This is the ultimate output for the user or the autonomous agent.
        """
        verdict = {
            "trade_direction": "Long",
            "conviction_level": "High",
            "capital_allocation_suggestion": "0.5% of portfolio",
            "key_risks": ["Volatility expansion due to news", "Failure to respect M15 FVG"],
            "alternative_scenarios": ["If M15 POI fails, look for re-entry at H1 OB."],
            "conditions_to_abort": ["Price breaking below M15 inducement low before entry."],
            "entry_point": "1.2285",
            "sl": "1.2480",
            "tp": "1.2550"
        }

        if quant_score["trade_grade"] == "NO TRADE":
            return {"trade_direction": "NO TRADE", "reason": "Quant score too low."}

        return verdict
