"""
Statistical & ML Models Module
==============================

Predictive models for greenwashing detection and market impact:
- Econometric models (Panel data, IV, DID, VAR)
- Machine learning predictors (Random Forest, XGBoost)
- Deep learning (Transformers, attention visualization)
- Time series analysis
"""

from .econometric import PanelDataAnalyzer, IVAnalyzer, DIDAnalyzer, VARAnalyzer, SurvivalAnalyzer
from .ml_predictor import MLPredictor, GreenwashingPredictionModel
from .transformer import TransformerAnalyzer, AttentionVisualizer, MultiTaskModel
from .time_series import TimeSeriesAnalyzer
from .advanced_models import (
    CompetitiveResonanceModel,
    WeeklyChurnDetector,
    PsychographicSegmenter,
    BundleOptimizer,
)

__all__ = [
    "PanelDataAnalyzer",
    "IVAnalyzer",
    "DIDAnalyzer",
    "VARAnalyzer",
    "SurvivalAnalyzer",
    "MLPredictor",
    "GreenwashingPredictionModel",
    "TransformerAnalyzer",
    "AttentionVisualizer",
    "MultiTaskModel",
    "TimeSeriesAnalyzer",
    "CompetitiveResonanceModel",
    "WeeklyChurnDetector",
    "PsychographicSegmenter",
    "BundleOptimizer",
]
