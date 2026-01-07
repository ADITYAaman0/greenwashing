"""
Financial Analysis Module
=========================

Financial modeling and investment strategies:
- Risk analysis and volatility
- Fama-French factor models
- Options implied volatility
- Long-short portfolio construction
"""

from .risk_analysis import RiskAnalyzer
from .fama_french import FameFrenchAnalyzer
from .options import OptionsAnalyzer
from .portfolio import GreenswashingPortfolio

__all__ = [
    "RiskAnalyzer",
    "FameFrenchAnalyzer",
    "OptionsAnalyzer",
    "GreenswashingPortfolio",
]
