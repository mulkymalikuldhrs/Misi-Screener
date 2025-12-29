class TraderAgent:
    """
    The central decision-making agent. It synthesizes reports from all analyst
    agents, selects a strategy, and generates a final trade proposal.
    """
    def __init__(self, strategy_library, risk_manager):
        self.strategy_library = strategy_library
        self.risk_manager = risk_manager

    def make_decision(self, analysis_reports):
        """
        Takes all analysis reports and makes a final trading decision.

        Args:
            analysis_reports: A dictionary containing the outputs from all
                              analyst agents (technical, fundamental, etc.).

        Returns:
            A final trade object, or None if no trade is taken.
        """
        # 1. Use an LLM to "think hard" about the combined analysis.
        #    - What is the overall market consensus?
        #    - Are there conflicting signals? (e.g., technicals bullish, fundamentals bearish)

        # 2. Select the most appropriate strategy from the strategy_library.
        #    - e.g., If sentiment is high and trend is up, select a momentum strategy.

        # 3. Generate a precise trade proposal.
        trade_proposal = {
            "asset": "BTC-USD",
            "action": "BUY",
            "entry_price": 60000,
            "stop_loss": 59000,
            "take_profit": 65000,
            "position_size": 1.0,
            "risk_per_trade": 0.01 # 1% of portfolio
        }

        # 4. Submit the proposal to the RiskManagerAgent for final approval.
        is_approved, reason = self.risk_manager.evaluate_trade(trade_proposal)

        if is_approved:
            print("Trade approved. Executing...")
            # 5. Execute the trade
            return trade_proposal
        else:
            print(f"Trade vetoed by Risk Manager: {reason}")
            return None
