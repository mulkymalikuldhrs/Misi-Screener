# components/final_verdict/engine.py

class FinalVerdictEngine:
    """
    MODULE 11: FINAL VERDICT
    Delivers the final, synthesized decision.

    Status: Stub — requires execution plan and quant score from other modules.
    """

    def __init__(self):
        self._configured = False

    def decide(self, execution_plan, quant_score):
        """
        Takes the final execution plan and score to generate a clear, final verdict.
        Returns 'not configured' state when no real inputs are available.
        """
        if not self._configured:
            # If quant_score is from an unconfigured QuantScoringEngine, it will have no grade
            if isinstance(quant_score, dict) and quant_score.get("status") == "not_configured":
                return {
                    "status": "not_configured",
                    "message": "FinalVerdictEngine: Cannot render verdict — quant scoring is not configured.",
                    "trade_direction": "NO TRADE",
                    "reason": "Insufficient analysis modules configured."
                }

            return {
                "status": "not_configured",
                "message": "FinalVerdictEngine: Not configured. Enable dependent modules first.",
                "trade_direction": None,
                "conviction_level": None
            }

        return self._render_verdict(execution_plan, quant_score)
