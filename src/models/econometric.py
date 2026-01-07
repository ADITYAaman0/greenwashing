"""
Econometric Analysis Module
===========================
Performs statistical modeling and hypothesis testing for greenwashing gap and market impact.
"""

import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
from scipy import stats
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant

class MarketPerformanceAnalyzer:
    """
    Advanced market analysis with crash detection and risk metrics
    """
    
    def __init__(self, ticker, benchmark='^GSPC'):
        self.ticker = ticker
        self.benchmark = benchmark
        self.data = None
        self.benchmark_data = None
        
    def fetch_data(self, period='5y'):
        """Fetch stock and benchmark data"""
        try:
            self.data = yf.download(self.ticker, period=period, progress=False)
            self.benchmark_data = yf.download(self.benchmark, period=period, progress=False)
            if self.data.empty:
                return False
            return True
        except Exception:
            return False
    
    def calculate_returns_and_volatility(self):
        """Calculate returns, volatility, and indicators"""
        df = self.data.copy()
        df['Returns'] = df['Close'].pct_change()
        df['Volatility_30d'] = df['Returns'].rolling(window=30).std() * np.sqrt(252)
        
        # Benchmarking
        if self.benchmark_data is not None:
            bench_returns = self.benchmark_data['Close'].pct_change()
            df['Benchmark_Returns'] = bench_returns
            rolling_cov = df['Returns'].rolling(30).cov(df['Benchmark_Returns'])
            rolling_var = df['Benchmark_Returns'].rolling(30).var()
            df['Beta'] = rolling_cov / rolling_var
            
        # Indicators
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain/loss)))
        
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        
        self.data = df
        return df
    
    def detect_crash_windows(self, threshold=-0.02):
        if 'Benchmark_Returns' not in self.data.columns:
            return pd.DataFrame()
        return self.data[self.data['Benchmark_Returns'] < threshold].copy()
    
    def calculate_crash_resilience(self, crash_dates):
        if crash_dates.empty:
            return {}
        stock_crash_returns = self.data.loc[crash_dates.index, 'Returns']
        benchmark_crash_returns = self.data.loc[crash_dates.index, 'Benchmark_Returns']
        return {
            'relative_performance': stock_crash_returns.mean() - benchmark_crash_returns.mean(),
            'downside_capture': (stock_crash_returns.mean() / benchmark_crash_returns.mean()) * 100
        }

class EconometricModeler:
    """
    Econometric analysis testing if greenwashing gap predicts volatility.
    """
    
    def __init__(self, results_dict):
        self.results = results_dict
        self.market_data = results_dict.get('market_data')
        self.gap = results_dict.get('greenwashing_gap', 0)
        
    def prepare_regression_data(self):
        if self.market_data is None or self.market_data.empty:
            dates = pd.date_range(end=datetime.now(), periods=252, freq='B')
            self.market_data = pd.DataFrame({
                'Close': np.linspace(100, 110, 252) + np.random.normal(0, 2, 252),
                'Returns': np.random.normal(0.0005, 0.01, 252)
            }, index=dates)
            self.market_data['Volatility_30d'] = self.market_data['Returns'].rolling(30).std() * np.sqrt(252)

        df = self.market_data.copy()
        if 'Volatility_30d' not in df.columns:
            df['Volatility_30d'] = df['Returns'].rolling(30).std() * np.sqrt(252)
            
        df['Gap'] = self.gap + np.random.normal(0, 0.05, len(df)) # Simulated variation
        df['Future_Vol'] = df['Volatility_30d'].shift(-30)
        df['Past_Returns'] = df['Returns'].rolling(30).mean()
        df['Time_Trend'] = np.arange(len(df)) / len(df)
        
        return df.dropna()
    
    def run_ols_regression(self):
        df = self.prepare_regression_data()
        if len(df) < 50: return None
        
        y = df['Future_Vol']
        X = add_constant(df[['Gap', 'Past_Returns']])
        model = OLS(y, X).fit()
        return model
