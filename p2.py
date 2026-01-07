"""
EcoSight Analytics: Legacy Entry Point
======================================
This file now serves as a wrapper for the modular src structure.
For the latest code, please refer to the modules in src/.
"""

import sys
import os

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import from modules
from src.collectors.sec_collector import SECDataCollector
from src.collectors.news_collector import EnhancedNewsCollector, NewsCollector
from src.analyzers.sentiment import MultiModelSentimentAnalyzer, EnsemblesentimentAnalyzer
from src.models.econometric import MarketPerformanceAnalyzer, EconometricModeler
from src.analyzers.greenwashing import GreenwashingAnalyzer, ComparativeAnalyzer
from src.models.advanced_models import TimeSeriesAnalyzer
from src.collectors.market_data import get_world_market_companies

if __name__ == "__main__":
    print("🌿 EcoSight Analytics: Modular Engine Loaded.")
    print("Run the dashboard using: streamlit run src/visualization/dashboard.py")