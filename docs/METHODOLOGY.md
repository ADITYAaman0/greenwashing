# Research Methodology

## Greenwashing Gap Analysis

### Definition

The **Greenwashing Gap** is defined as the difference between:
- **Internal Sentiment**: What companies claim in official disclosures (SEC filings, ESG reports)
- **External Sentiment**: How the public and media perceive the company's ESG performance

```
Gap Score = Internal Sentiment - External Sentiment
```

### Interpretation

| Gap Score | Interpretation |
|-----------|----------------|
| > 0.3 | High greenwashing risk - Claims exceed reality |
| 0.1 to 0.3 | Moderate concern - Some discrepancy |
| -0.1 to 0.1 | Aligned - Claims match perception |
| < -0.1 | Under-reporting - Company is modest about ESG |

## Data Sources

### Internal (Company Claims)
1. **SEC 10-K Filings** - Annual reports with sustainability sections
2. **DEF 14A** - Proxy statements with governance info
3. **8-K Filings** - Material event disclosures
4. **Sustainability Reports** - Voluntary ESG disclosures

### External (Public Perception)
1. **News Articles** - Media coverage and analysis
2. **ESG Ratings** - MSCI, Sustainalytics, S&P Global
3. **NGO Reports** - Environmental group assessments
4. **Social Media** - Public sentiment on platforms

## NLP Methodology

### Sentiment Analysis
- Primary: FinBERT (financial domain-specific)
- Ensemble: RoBERTa, VADER for validation
- Output: Score from -1 (negative) to +1 (positive)

### Aspect-Based Analysis
Separate sentiment for each ESG pillar:
- **Environmental**: emissions, climate, energy, waste
- **Social**: labor, diversity, community, health
- **Governance**: board, ethics, transparency, risk

## Statistical Models

### Causal Inference
- **Panel Data**: Fixed effects for company characteristics
- **Instrumental Variables**: Address reverse causality
- **Difference-in-Differences**: Event study for scandals

### Prediction
- **Random Forest**: Feature importance for risk factors
- **XGBoost**: Gradient boosting for crash prediction
- **SHAP**: Explainable AI for model interpretation

## Market Impact

### Metrics Analyzed
- Stock volatility (30-day, 90-day)
- Abnormal returns during ESG events
- Trading volume changes
- Implied volatility from options

### Investment Strategy
Long-short portfolio based on gap scores has shown:
- Alpha generation during market stress
- Lower drawdowns for low-gap companies
- Predictive value for ESG-related events
