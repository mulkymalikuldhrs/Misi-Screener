import argparse
import pandas as pd
from tqdm import tqdm

# Ensure all modules can be imported
from agents.signal_agent import SignalAgent
from agents.technical_analyst import TechnicalAnalystAgent
from agents.portfolio_manager import PortfolioManager
from agents.hedge_fund_master_agent import HedgeFundMasterAgent
from agents.strategy_manager import StrategyManager
from agents.risk_manager import RiskManager
from execution.paper_trading_broker import PaperTradingBroker
from data_sources.yfinance_connector import YFinanceConnector


# --- Backtesting "Broker" ---
# We need a modified broker for backtesting that uses historical data instead of live prices.
class BacktestingBroker(PaperTradingBroker):
    def __init__(self, portfolio_manager, historical_data, data_connector):
        super().__init__(portfolio_manager=portfolio_manager, data_connector=data_connector)
        self.historical_data = historical_data
        self.current_step = 0

    def _get_current_price(self, ticker: str) -> float:
        """Overrides the live broker to return the price at the current backtest step."""
        return self.historical_data['Close'].iloc[self.current_step]

    def set_step(self, step: int):
        """Sets the current time step for the backtest."""
        self.current_step = step


def run_backtest(strategy_filepath: str, start_date: str, end_date: str):
    """
    Runs a historical backtest for a given strategy.

    Args:
        strategy_filepath (str): Path to the strategy YAML file.
        start_date (str): The start date for the backtest (YYYY-MM-DD).
        end_date (str): The end date for the backtest (YYYY-MM-DD).
    """
    print(f"--- Starting Backtest for {strategy_filepath} ---")
    print(f"Period: {start_date} to {end_date}")

    # 1. --- Initialization ---
    data_connector = YFinanceConnector()
    technical_analyst = TechnicalAnalystAgent()
    strategy_manager = StrategyManager(strategy_filepath)

    portfolio_manager = PortfolioManager(data_connector=data_connector, initial_cash=100000.0)

    # Load the strategy to get the ticker
    ticker = strategy_manager.get_asset_ticker()

    # Fetch all historical data for the backtest period at once
    full_historical_data = data_connector.get_historical_data(ticker, period="max")
    backtest_data = full_historical_data[start_date:end_date]
    if backtest_data.empty:
        print("Error: No historical data found for the specified date range.")
        return

    # Create the backtesting-specific components
    backtesting_broker = BacktestingBroker(portfolio_manager, backtest_data, data_connector)

    # 2. --- Simulation Loop ---
    # We iterate through each data point in our historical dataset.
    print(f"\nRunning simulation over {len(backtest_data)} data points...")
    for i in tqdm(range(len(backtest_data))):
        # Create a "view" of the data up to the current point in time
        # This simulates the agent only having access to past data
        current_data_view = backtest_data.iloc[:i+1]

        # We need a mock data connector that returns this historical view
        class HistoricalDataConnector:
            def __init__(self, data_view):
                self.data_view = data_view

            def get_historical_data(self, ticker, period="1y"):
                return self.data_view

        historical_connector = HistoricalDataConnector(current_data_view)

        # Instantiate agents with the historical data view
        strategy_mgr = StrategyManager(strategy_filepath)
        signal_agent = SignalAgent(
            strategy_manager=strategy_mgr,
            data_connector=historical_connector,
            technical_analyst=technical_analyst
        )
        risk_manager = RiskManager(
            data_connector=historical_connector,
            technical_analyst=technical_analyst
        )

        # The master agent orchestrates a single "turn"
        master_agent = HedgeFundMasterAgent(
            strategy_manager=strategy_mgr,
            signal_agent=signal_agent,
            portfolio_manager=portfolio_manager,
            risk_manager=risk_manager,
            broker=backtesting_broker
        )

        # Set the current time step for the broker to get the correct price
        backtesting_broker.set_step(i)

        # Run a single trading loop iteration (synchronous for backtesting)
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If already in an async context, create a task
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    pool.submit(lambda: asyncio.run(master_agent.run_trading_loop())).result()
            else:
                loop.run_until_complete(master_agent.run_trading_loop())
        except RuntimeError:
            asyncio.run(master_agent.run_trading_loop())

    # 3. --- Performance Report ---
    print("\n--- Backtest Complete ---")
    final_state = portfolio_manager.get_state()
    print(f"Initial Portfolio Value: ${portfolio_manager.initial_cash:,.2f}")
    print(f"Final Portfolio Value:   ${final_state['portfolio_value']:,.2f}")

    total_return = (final_state['portfolio_value'] - portfolio_manager.initial_cash) / portfolio_manager.initial_cash
    print(f"Total Return: {total_return:.2%}")
    print(f"Total Trades: {final_state['trade_count']}")

    # TODO: Add more advanced metrics like Sharpe Ratio, Max Drawdown, etc.


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a backtest for a trading strategy.")
    parser.add_argument("strategy_file", help="Path to the strategy YAML file (e.g., strategies/mean_reversion_rsi.yml)")
    parser.add_argument("--start", default="2023-01-01", help="Start date in YYYY-MM-DD format")
    parser.add_argument("--end", default="2023-12-31", help="End date in YYYY-MM-DD format")

    args = parser.parse_args()

    run_backtest(args.strategy_file, args.start, args.end)
