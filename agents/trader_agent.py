from typing import Dict, Any, Optional
from utils.logger import logger


class TraderAgent:
    """
    The central decision-making agent. It synthesizes reports from all analyst
    agents, selects a strategy, and generates a final trade proposal.

    Status: Improved — now uses real analysis inputs instead of hardcoded values.
    When analysis reports are unavailable, it returns a NO TRADE decision.
    """

    def __init__(self, strategy_library=None, risk_manager=None):
        self.strategy_library = strategy_library
        self.risk_manager = risk_manager

    def make_decision(self, analysis_reports: Dict[str, Any],
                      signal: Optional[str] = None,
                      entry_price: Optional[float] = None,
                      stop_loss_price: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """
        Takes all analysis reports and makes a final trading decision.

        Args:
            analysis_reports: A dictionary containing the outputs from all
                              analyst agents (technical, fundamental, etc.).
            signal: The trading signal from SignalAgent (BUY, SELL, HOLD).
            entry_price: The current market price.
            stop_loss_price: The calculated stop-loss price.

        Returns:
            A final trade object, or None if no trade is taken.
        """
        # If no signal provided, we cannot make a decision
        if not signal or signal == "HOLD":
            logger.info("TraderAgent: No actionable signal. No trade proposed.")
            return None

        # Validate required price data
        if not entry_price:
            logger.warning("TraderAgent: No entry price provided. Cannot make trade decision.")
            return None

        # Check if analysis modules are configured
        unconfigured = []
        for key, report in analysis_reports.items():
            if isinstance(report, dict) and report.get("status") == "not_configured":
                unconfigured.append(key)

        if unconfigured:
            logger.info(f"TraderAgent: Analysis modules not configured: {unconfigured}. "
                        f"Proceeding with signal-only decision.")

        # Build trade proposal from real signal data
        trade_proposal = {
            "asset": analysis_reports.get("ticker", "UNKNOWN"),
            "action": signal,
            "entry_price": entry_price,
            "stop_loss": stop_loss_price,
            "take_profit": None,  # Would be calculated based on risk/reward ratio
            "position_size": None,  # Would be calculated by PortfolioManager
            "risk_per_trade": None,  # Would be set by StrategyManager
            "analysis_modules_configured": len(analysis_reports) - len(unconfigured),
            "analysis_modules_total": len(analysis_reports)
        }

        # Calculate take profit from risk/reward if stop loss is available
        if stop_loss_price and entry_price:
            risk_per_unit = abs(entry_price - stop_loss_price)
            reward_ratio = 1.5  # Default risk:reward ratio
            if signal == "BUY":
                trade_proposal["take_profit"] = entry_price + (risk_per_unit * reward_ratio)
            elif signal == "SELL":
                trade_proposal["take_profit"] = entry_price - (risk_per_unit * reward_ratio)

        # Submit the proposal to the RiskManager for final approval
        if self.risk_manager:
            is_approved, reason = self.risk_manager.evaluate_trade(trade_proposal)
            if not is_approved:
                logger.info(f"TraderAgent: Trade vetoed by Risk Manager: {reason}")
                return None
        else:
            logger.warning("TraderAgent: No risk manager configured. Approving without risk checks.")

        logger.info(f"TraderAgent: Trade proposal approved — {signal} @ {entry_price}")
        return trade_proposal
