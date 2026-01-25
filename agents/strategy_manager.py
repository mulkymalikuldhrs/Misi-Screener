import yaml
from typing import Dict, Any

class StrategyManager:
    """
    Manages the loading and parsing of trading strategies from YAML files.
    This decouples the strategy definition from the agents that execute it.
    """

    def __init__(self, strategy_filepath: str):
        """
        Initializes the manager and loads the specified strategy.

        Args:
            strategy_filepath (str): The path to the strategy YAML file.
        """
        self.strategy = self._load_strategy(strategy_filepath)
        print(f"StrategyManager: Successfully loaded strategy '{self.strategy.get('strategy_name', 'Unnamed')}'")

    def _load_strategy(self, filepath: str) -> Dict[str, Any]:
        """
        Loads and parses the strategy YAML file.

        Args:
            filepath (str): The path to the YAML file.

        Returns:
            A dictionary containing the strategy configuration.
        """
        try:
            with open(filepath, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: Strategy file not found at {filepath}")
            raise
        except Exception as e:
            print(f"Error loading or parsing strategy file {filepath}: {e}")
            raise

    def get_strategy(self) -> Dict[str, Any]:
        """
        Returns the loaded strategy dictionary.
        """
        return self.strategy
