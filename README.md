# � EcoSight Analytics: Advanced Greenwashing Detection

## 📌 Problem Statement
Corporations increasingly use "green" claims to appeal to eco-conscious investors and consumers. However, many these claims are unsubstantiated or misleading—a practice known as **greenwashing**. Greenwashing creates market distortions, misallocates capital, and hides regulatory risks from stakeholders.

## 🚀 Solution
EcoSight Analytics provides an automated, data-driven pipeline to detect greenwashing by analyzing the **divergence (Gap)** between a company's internal claims and external reality.

### Key Features
- **Internal Analysis:** Scraping ESG commitments from SEC EDGAR filings (10-K/10-Q).
- **Public Perception:** Aggregating global news sentiment via multiple APIs (Yahoo, Google, NewsAPI).
- **Transformer NLP:** Using FinBERT and EnvironmentalBERT to compute precise sentiment scores.
- **Econometric Modeling:** Regressing the "Greenwashing Gap" against market volatility and crash resilience.
- **ML Prediction:** Predicting future stock volatility and regulatory risk using Random Forest ensembles.

## 📁 Repository Structure
```text
├── results/              # Analysis outputs, reports, and visualization artifacts
├── src/
│   ├── collectors/       # Data acquisition: SEC, News, Market Data, ESG Ratings
│   ├── analyzers/        # Core engines: Sentiment, Temporal, Greenwashing orchestration
│   ├── models/           # Analytical models: Econometrics, ML Predictors, Advanced Dynamics
│   └── visualization/    # User interface: Streamlit dashboard
├── p2.py                 # Modular entry point wrapper
└── README.md             # Documentation
```

## 📊 Model Evaluation & Metrics
- **Greenwashing Gap:** `Internal Sentiment - External Sentiment`. Gaps > 0.3 are flagged as "High Risk".
- **Statistical Significance:** Welch's t-test and Cohen's d for effect size.
- **ML Performance:** Random Forest R² score used to measure predictability of volatility based on ESG features.

## 🚦 Getting Started
1. **Clone the Repo:** `git clone https://x:/gap`
2. **Install Dependencies:** `pip install -r requirements.txt`
3. **Run Dashboard:** `streamlit run src/visualization/dashboard.py`

## �️ Data Sources
- **SEC Filings:** Official corporate disclosures (EDGAR).
- **Financial News:** Real-time sentiment via Yahoo Finance & Bloomberg.
- **Market Data:** Historical prices and volatility via yfinance.
- **ESG Ratings:** Benchmark scores from MSCI and Sustainalytics.
