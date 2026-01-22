import threading
from typing import Any, Dict, List

# Absolute imports from the project root
from agents.master_agent import HedgeFundMasterAgent
from agents.portfolio_manager import PortfolioManager
from agents.risk_manager import RiskManager
from agents.signal_agent import SignalAgent
from agents.strategy_manager import StrategyManager
from data_sources.yfinance_connector import YFinanceConnector
from execution.paper_trading_broker import PaperTradingBroker

class HedgeFund:
    """
    Represents the entire hedge fund, encapsulating all trading components,
    state, and logic into a single, cohesive unit.
    """
    def __init__(self, initial_cash: float = 100000.0):
        # --- Core Components ---
        self.strategy_manager = StrategyManager()
        self.data_connector = YFinanceConnector()
        self.risk_manager = RiskManager(data_connector=self.data_connector)
        self.portfolio_manager = PortfolioManager(initial_cash=initial_cash)
        self.broker = PaperTradingBroker(
            portfolio_manager=self.portfolio_manager,
            data_connector=self.data_connector
        )

        # --- State Variables ---
        self.master_agent: HedgeFundMasterAgent = None
        self.agent_thread: threading.Thread = None
        self.is_running: bool = False

    def start_agent(self, strategy_name: str, interval_seconds: int = 60):
        """
        Initializes and starts the HedgeFundMasterAgent in a background thread.

        Args:
            strategy_name (str): The name of the strategy to execute.
            interval_seconds (int): The loop interval for the trading agent.

        Raises:
            ValueError: If the agent is already running or the strategy is not found.
        """
        if self.is_running:
            raise ValueError("Agent is already running.")

        # 1. Load the strategy
        strategy_config = self.strategy_manager.get_strategy(strategy_name)

        # 2. Initialize the SignalAgent with the chosen strategy
        signal_agent = SignalAgent(
            strategy_config=strategy_config,
            data_connector=self.data_connector
        )

        # 3. Initialize the MasterAgent
        self.master_agent = HedgeFundMasterAgent(
            signal_agent=signal_agent,
            portfolio_manager=self.portfolio_manager,
            broker=self.broker,
            risk_manager=self.risk_manager, # Inject the RiskManager
            strategy=strategy_config
        )

        # 4. Start the agent loop in a background thread
        self.is_running = True
        self.agent_thread = threading.Thread(
            target=self.master_agent.start,
            args=(interval_seconds,)
        )
        self.agent_thread.daemon = True
        self.agent_thread.start()
        print(f"HedgeFund: Master Agent started with strategy '{strategy_name}'.")

    def stop_agent(self):
        """
        Stops the master agent's trading loop gracefully.
        """
        if not self.is_running or not self.master_agent:
            raise ValueError("Agent is not currently running.")

        self.master_agent.stop()
        self.is_running = False
        self.master_agent = None
        self.agent_thread = None
        print("HedgeFund: Master Agent stopped.")

    def get_agent_status(self) -> Dict:
        """Returns the current status of the trading agent."""
        return {
            "is_running": self.is_running,
            "strategy": self.master_agent.strategy.get('strategy_name', 'N/A') if self.master_agent else 'N/A',
            "asset_ticker": self.master_agent.strategy.get('asset_ticker', 'N/A') if self.master_agent else 'N/A'
        }

    def get_portfolio_state(self) -> Dict:
        """Retrieves the current state of the portfolio."""
        return self.portfolio_manager.get_state()

    def get_trade_history(self) -> List[Dict]:
        """Retrieves the trade history from the broker."""
        return self.broker.get_trade_history()

    def list_strategies(self) -> List[str]:
        """Returns a list of all available strategy names."""
        return self.strategy_manager.list_strategies()
