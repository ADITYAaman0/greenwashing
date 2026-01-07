"""
Visualization Module
====================

Reporting and visualization tools:
- Matplotlib/Seaborn static plots
- Plotly interactive charts
- Markdown/PDF report generation
- Streamlit dashboard
"""

from .reports import ReportGenerator
from .plots import PlotGenerator
# Dashboard is typically run as a script, not imported

__all__ = [
    "ReportGenerator",
    "PlotGenerator",
]
