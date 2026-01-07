"""
External Perception Module
==========================
Aggregates public perception data from news, social media, and stakeholders.
"""

class ExternalPerceptionCollector:
    """
    Multi-channel public perception data aggregator.
    """
    
    def __init__(self, ticker, company_name):
        self.ticker = ticker
        self.company_name = company_name
    
    def get_external_data_map(self):
        """Map of external voices on company ESG practices"""
        return {
            'Traditional News': ['Bloomberg', 'Reuters', 'WSJ', 'FT'],
            'Social Media': ['Twitter/X', 'Reddit', 'LinkedIn'],
            'Stakeholder Voices': ['Glassdoor', 'NGO Reports'],
            'Regulatory': ['SEC Comment Letters', 'FTC Complaints']
        }
    
    def calculate_weighted_sentiment(self, source_sentiments):
        """Weights sources by credibility"""
        weights = {
            'News': 0.4,
            'NGO': 0.3,
            'Ratings': 0.3
        }
        return sum(weights.get(k, 0) * v for k, v in source_sentiments.items())
