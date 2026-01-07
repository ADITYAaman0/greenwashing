"""
Machine Learning Prediction Module
==================================
Predicts market volatility using ESG and sentiment features through ensemble models.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class MLPredictor:
    """
    Random Forest model for predicting future volatility.
    """
    
    def __init__(self, data):
        self.df = data
        self.model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        
    def train_and_predict(self, features=None):
        if self.df is None or len(self.df) < 20:
            return None
            
        if features is None:
            features = ['Gap', 'Returns', 'Volatility_30d', 'Time_Trend']
            
        # Filter existing features
        features = [f for f in features if f in self.df.columns]
        if not features: return None
        
        X = self.df[features]
        y = self.df['Future_Vol'] if 'Future_Vol' in self.df.columns else None
        
        if y is None: return None
        
        # Split (Time-series aware)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        
        self.model.fit(X_train, y_train)
        score = self.model.score(X_test, y_test)
        
        importances = pd.DataFrame({
            'Feature': features,
            'Importance': self.model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        return {
            'score': score,
            'importances': importances,
            'model': self.model
        }
