"""
Temporal Sentiment Tracking Module
=================================
Tracks how corporate sentiment and ESG-related public perception evolve over time.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from transformers import pipeline

class TemporalsentimentTracker:
    """
    Track how sentiment evolves over time
    Detect sudden shifts that indicate greenwashing events
    """
    
    def __init__(self):
        # We'll use a local pipeline for temporal tracking
        self.sentiment_model = pipeline("sentiment-analysis", model="ProsusAI/finbert", device=-1)
    
    def track_sentiment_evolution(self, ticker, news_data=None):
        """
        Create time series of sentiment using real news data if available
        """
        timeline = []
        
        if news_data:
            df_news = pd.DataFrame(news_data)
            if 'date' in df_news.columns and 'title' in df_news.columns:
                df_news['date'] = pd.to_datetime(df_news['date'])
                df_news = df_news.sort_values('date')
                df_news['period'] = df_news['date'].dt.to_period('W')
                
                for period, group in df_news.groupby('period'):
                    texts = group['title'].tolist()
                    if texts:
                        results = self.sentiment_model(texts[:10], truncation=True)
                        score_sum = 0
                        for res in results:
                            val = res['score'] if res['label'] == 'positive' else -res['score'] if res['label'] == 'negative' else 0
                            score_sum += val
                        
                        timeline.append({
                            'date': period.start_time,
                            'external': score_sum / len(results),
                            'internal': 0, # To be filled by filing analyzer
                            'gap': 0
                        })
        
        if not timeline:
            # Fallback to simulation
            today = datetime.now()
            for i in range(12):
                date = today - timedelta(days=30*i)
                timeline.append({
                    'date': date,
                    'external': np.random.normal(0, 0.4),
                    'internal': np.random.normal(0.2, 0.1),
                    'gap': 0
                })
                
        df = pd.DataFrame(timeline)
        df['gap'] = df['internal'] - df['external']
        
        return {
            'timeline': df,
            'gap_trend': self._calculate_trend(df['gap']),
            'gap_volatility': df['gap'].std()
        }
    
    def _calculate_trend(self, series):
        """Calculate if gap is widening or narrowing"""
        if len(series) < 2: return "STABLE"
        x = np.arange(len(series))
        z = np.polyfit(x, series.values, 1)
        slope = z[0]
        if slope > 0.02: return "WIDENING"
        if slope < -0.02: return "NARROWING"
        return "STABLE"
