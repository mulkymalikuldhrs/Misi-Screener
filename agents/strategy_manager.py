import os
import yaml
from typing import Dict, List

class StrategyManager:
    """
    Manages the loading and retrieval of trading strategies from YAML files.
    """
    def __init__(self, strategies_dir: str = "strategies"):
        """
        Initializes the StrategyManager.

        Args:
            strategies_dir (str): The directory where strategy YAML files are located.
        """
        self.strategies_dir = strategies_dir
        self.strategies: Dict[str, Dict] = self._load_strategies()

    def _load_strategies(self) -> Dict[str, Dict]:
        """
        Scans the strategies directory, loads all valid YAML files, and stores them.
        """
        loaded_strategies = {}
        if not os.path.isdir(self.strategies_dir):
            print(f"StrategyManager: Warning: Directory '{self.strategies_dir}' not found.")
            return loaded_strategies

        for filename in os.listdir(self.strategies_dir):
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                filepath = os.path.join(self.strategies_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        strategy_data = yaml.safe_load(f)
                        # Use the filename (without extension) as the strategy name
                        strategy_name = os.path.splitext(filename)[0]
                        loaded_strategies[strategy_name] = strategy_data
                        print(f"StrategyManager: Successfully loaded strategy '{strategy_name}' from {filename}")
                except yaml.YAMLError as e:
                    print(f"StrategyManager: Error loading YAML from {filepath}: {e}")
                except Exception as e:
                    print(f"StrategyManager: An unexpected error occurred loading {filepath}: {e}")

        return loaded_strategies

    def get_strategy(self, name: str) -> Dict:
        """
        Retrieves a loaded strategy by its name.

        Args:
            name (str): The name of the strategy (filename without extension).

        Returns:
            Dict: The strategy configuration dictionary.

        Raises:
            ValueError: If the strategy name is not found.
        """
        strategy = self.strategies.get(name)
        if not strategy:
            raise ValueError(f"Strategy '{name}' not found. Available strategies: {self.list_strategies()}")
        return strategy

    def list_strategies(self) -> List[str]:
        """
        Returns a list of all available strategy names.
        """
        return list(self.strategies.keys())
