# API Reference
===============

## Collectors

### SECDataCollector

```python
from src.collectors import SECDataCollector

collector = SECDataCollector(cik="0000320193", company_name="Apple Inc.")
filings = collector.get_filing_urls(form_type='10-K', count=3)
esg_text = collector.extract_esg_text(filing_url)
```

### EnhancedNewsCollector

```python
from src.collectors import EnhancedNewsCollector

collector = EnhancedNewsCollector(company_name="Apple Inc.", ticker="AAPL")
news = collector.get_esg_focused_news()
```

## Analyzers

### MultiModelSentimentAnalyzer

```python
from src.analyzers import MultiModelSentimentAnalyzer

analyzer = MultiModelSentimentAnalyzer()
scores = analyzer.compute_sentiment_score(texts)
```

### AspectBasedESGAnalyzer

```python
from src.analyzers import AspectBasedESGAnalyzer

analyzer = AspectBasedESGAnalyzer()
breakdown = analyzer.analyze_by_esg_pillar(text)
# Returns: {'Environmental': score, 'Social': score, 'Governance': score}
```

## Models

### MLPredictor

```python
from src.models import MLPredictor

predictor = MLPredictor()
predictor.train_model(comparative_results)
prediction = predictor.predict_crash_performance(new_company_results)
```

## Financial

### GreenswashingPortfolio

```python
from src.financial import GreenswashingPortfolio

portfolio = GreenswashingPortfolio()
positions = portfolio.construct_long_short_portfolio(companies, gap_threshold=0.3)
returns = portfolio.backtest_strategy(portfolio, start_date, end_date)
```
