"""
Market Data Utils
=================
Metadata and collection helpers for market sectors and companies.
"""

def get_world_market_companies():
    """
    Returns a dictionary of sectors and their constituent major companies.
    Used for comparative analysis and target selection.
    """
    return {
        "Technology": [
            {"ticker": "AAPL", "name": "Apple Inc.", "cik": "0000320193"},
            {"ticker": "MSFT", "name": "Microsoft Corp.", "cik": "0000789019"},
            {"ticker": "GOOGL", "name": "Alphabet Inc.", "cik": "0001652044"},
            {"ticker": "NVDA", "name": "NVIDIA Corporation", "cik": "0001045810"},
            {"ticker": "TSLA", "name": "Tesla, Inc.", "cik": "0001318605"}
        ],
        "Energy": [
            {"ticker": "XOM", "name": "Exxon Mobil Corp.", "cik": "0000034088"},
            {"ticker": "CVX", "name": "Chevron Corp.", "cik": "0000093461"},
            {"ticker": "SHEL", "name": "Shell plc", "cik": "0001306965"},
            {"ticker": "BP", "name": "BP p.l.c.", "cik": "0000313807"},
            {"ticker": "TTE", "name": "TotalEnergies SE", "cik": "0000879764"}
        ],
        "Consumer Staples": [
            {"ticker": "PG", "name": "Procter & Gamble Co.", "cik": "0000080424"},
            {"ticker": "KO", "name": "Coca-Cola Co.", "cik": "0000021344"},
            {"ticker": "PEP", "name": "PepsiCo, Inc.", "cik": "0000077476"},
            {"ticker": "WMT", "name": "Walmart Inc.", "cik": "0000104169"},
            {"ticker": "UL", "name": "Unilever PLC", "cik": "0000032906"}
        ],
        "Finance": [
            {"ticker": "JPM", "name": "JPMorgan Chase & Co.", "cik": "0000019617"},
            {"ticker": "BAC", "name": "Bank of America Corp.", "cik": "0000070852"},
            {"ticker": "WFC", "name": "Wells Fargo & Co.", "cik": "0000072971"},
            {"ticker": "GS", "name": "Goldman Sachs Group", "cik": "0000805676"},
            {"ticker": "MS", "name": "Morgan Stanley", "cik": "0000895421"}
        ]
    }
