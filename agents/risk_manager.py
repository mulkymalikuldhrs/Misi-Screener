class RiskManagerAgent:
    """
    Evaluates trade proposals and monitors the overall portfolio to ensure
    adherence to risk management rules. Has final veto power over any trade.
    """
    def __init__(self, portfolio_state, risk_rules):
        self.portfolio_state = portfolio_state
        self.risk_rules = risk_rules # e.g., max_drawdown, max_exposure_per_asset

    def evaluate_trade(self, trade_proposal):
        """
        Takes a trade proposal and decides whether to approve or veto it.

        Args:
            trade_proposal: A dictionary containing the details of the proposed trade
                           (asset, entry, stop_loss, position_size).

        Returns:
            A boolean (True for approve, False for veto) and a reason.
        """
        # 1. Check if the proposed trade violates any hard limits (e.g., max size)
        # 2. Simulate the impact of the trade on the portfolio's overall risk
        # 3. Check against portfolio-level rules (e.g., max drawdown)

        is_approved = True
        reason = "Trade is within all risk parameters."

        # Example rule:
        if trade_proposal['risk_per_trade'] > self.risk_rules['max_risk_per_trade']:
            is_approved = False
            reason = "Trade risk exceeds the maximum allowed risk per trade."

        return is_approved, reason
