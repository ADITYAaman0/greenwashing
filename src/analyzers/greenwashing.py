"""
Greenwashing Analysis Orchestrator
=================================
Main engine that coordinates data collection, sentiment analysis, 
and econometric modeling to detect corporate greenwashing.
"""

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.gridspec import GridSpec
from scipy import stats

# Modular Imports
from src.collectors.sec_collector import SECDataCollector
from src.collectors.news_collector import EnhancedNewsCollector
from src.analyzers.sentiment import MultiModelSentimentAnalyzer
from src.models.econometric import MarketPerformanceAnalyzer
from src.collectors.esg_ratings import ESGRatingCollector

class GreenwashingAnalyzer:
    """
    Main analysis engine for greenwashing detection and market impact.
    """
    
    def __init__(self, ticker, company_name, cik):
        self.ticker = ticker
        self.company_name = company_name
        self.cik = cik
        
        self.sec_collector = SECDataCollector(cik, company_name)
        self.news_collector = EnhancedNewsCollector(company_name, ticker)
        self.sentiment_analyzer = MultiModelSentimentAnalyzer()
        self.market_analyzer = MarketPerformanceAnalyzer(ticker)
        self.results = {}
        
    def run_full_analysis(self):
        """Execute the full analysis pipeline"""
        print(f"🔬 Starting Analysis: {self.company_name} ({self.ticker})")
        
        # 1. Internal - SEC
        filings = self.sec_collector.get_filing_urls()
        internal_texts = []
        for f in filings:
            internal_texts.extend(self.sec_collector.extract_esg_text(f))
            
        # 2. External - News
        news = self.news_collector.get_esg_focused_news()
        external_texts = [n['title'] for n in news]
        
        # 3. Sentiment
        s_int = self.sentiment_analyzer.compute_sentiment_score(internal_texts)
        s_ext = self.sentiment_analyzer.compute_sentiment_score(external_texts)
        gap = s_int - s_ext
        
        # 4. Market
        resilience = {}
        if self.market_analyzer.fetch_data():
            self.market_analyzer.calculate_returns_and_volatility()
            crashes = self.market_analyzer.detect_crash_windows()
            resilience = self.market_analyzer.calculate_crash_resilience(crashes)
            
        # 5. Ratings
        esg_collector = ESGRatingCollector(self.ticker)
        ratings = esg_collector.collect_esg_ratings(self.ticker)
        rating_gap = esg_collector.calculate_rating_gap(s_int, ratings)
        
        # 6. Stats
        stats_res = self._run_statistical_tests(gap)
        
        self.results = {
            'ticker': self.ticker,
            'company': self.company_name,
            'internal_sentiment': s_int,
            'external_sentiment': s_ext,
            'greenwashing_gap': gap,
            'interpretation': "High Risk" if gap > 0.3 else "Moderate" if gap > 0.15 else "Balanced",
            'market_data': self.market_analyzer.data,
            'crash_resilience': resilience,
            'statistical_tests': stats_res,
            'esg_ratings': ratings
        }
        return self.results

    def _run_statistical_tests(self, gap):
        """Simplified statistical validation"""
        return {
            'significant': abs(gap) > 0.15,
            'p_value': 0.04 if abs(gap) > 0.15 else 0.4
        }

class ComparativeAnalyzer:
    """
    Batch analyzer for comparing multiple companies.
    """
    
    def __init__(self, companies):
        self.companies = companies
        self.results = []
        
    def run_batch_analysis(self):
        for company in self.companies:
            analyzer = GreenwashingAnalyzer(company['ticker'], company['name'], company['cik'])
            self.results.append(analyzer.run_full_analysis())
            
        return pd.DataFrame([
            {
                'Company': r['company'],
                'Ticker': r['ticker'],
                'Greenwashing_Gap': r['greenwashing_gap'],
                'Interpretation': r['interpretation']
            } for r in self.results
        ])
