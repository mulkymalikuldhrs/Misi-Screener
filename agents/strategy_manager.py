import yaml
from typing import Dict, Any
from utils.logger import logger

class StrategyManager:
    """
    Loads, parses, and manages strategy configurations from YAML files.
    This class decouples strategy definitions from the core trading logic,
    allowing the system to be strategy-agnostic.
    """

    def __init__(self, strategy_filepath: str):
        """
        Initializes the manager with a specific strategy file.

        Args:
            strategy_filepath (str): The path to the strategy YAML file.
        """
        self.strategy = self._load_strategy(strategy_filepath)

    def _load_strategy(self, filepath: str) -> Dict[str, Any]:
        """
        Loads and parses the strategy YAML file.

        Args:
            filepath (str): The path to the YAML file.

        Returns:
            A dictionary containing the strategy configuration.

        Raises:
            FileNotFoundError: If the strategy file cannot be found.
            Exception: For any other errors during file parsing.
        """
        try:
            with open(filepath, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.error(f"Strategy file not found at {filepath}")
            raise
        except Exception as e:
            logger.error(f"Error loading or parsing strategy file {filepath}: {e}")
            raise

    def get_strategy_name(self) -> str:
        """Returns the name of the loaded strategy."""
        return self.strategy.get('name', 'Unnamed Strategy')

    def get_asset_ticker(self) -> str:
        """Returns the target asset ticker for the strategy."""
        return self.strategy.get('asset_ticker')

    def get_asset_tickers(self) -> list:
        """Returns a list of target asset tickers for the strategy."""
        tickers = self.strategy.get('asset_tickers')
        if tickers:
            return tickers
        single_ticker = self.strategy.get('asset_ticker')
        return [single_ticker] if single_ticker else []

    def get_strategy_parameters(self) -> Dict[str, Any]:
        """Returns the technical parameters for the strategy."""
        return self.strategy.get('parameters', {})

    def get_risk_management_rules(self) -> Dict[str, Any]:
        """Returns the risk management rules for the strategy."""
        return self.strategy.get('risk_management', {})
