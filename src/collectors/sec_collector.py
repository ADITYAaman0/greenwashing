"""
SEC Data Collector Module
========================
Handles extraction and parsing of SEC EDGAR filings for ESG disclosure analysis.
"""

import requests
import time
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.parse import quote_plus

class SECDataCollector:
    """
    Advanced SEC EDGAR data collector with multi-year support and better parsing
    """
    
    def __init__(self, cik, company_name):
        self.cik = cik.zfill(10)  # Pad CIK to 10 digits
        self.company_name = company_name
        self.headers = {
            'User-Agent': 'Academic Research Project contact@university.edu',
            'Accept-Encoding': 'gzip, deflate'
        }
        
    def get_filing_urls(self, form_type='10-K', count=3):
        """
        Retrieve URLs for the most recent filings of a specific type
        """
        if self.cik == "0000000000":
            print(f"   [WARNING] No valid CIK provided. Skipping SEC extraction.")
            return []
            
        # SEC EDGAR API endpoint - CIK must have leading zeros
        url = f"https://data.sec.gov/submissions/CIK{self.cik}.json"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            time.sleep(0.15)  # SEC rate limit: ~7 requests/second to be safe
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    filings = data.get('filings', {}).get('recent', {})
                    
                    if not filings or 'form' not in filings:
                        print(f"   [WARNING]  No filings data found in response")
                        return []
                    
                    # Filter for desired form type
                    filing_urls = []
                    forms = filings.get('form', [])
                    accessions = filings.get('accessionNumber', [])
                    primary_docs = filings.get('primaryDocument', [])
                    dates = filings.get('filingDate', [])
                    
                    for i, form in enumerate(forms):
                        if form == form_type and len(filing_urls) < count and i < len(accessions):
                            try:
                                accession = accessions[i].replace('-', '')
                                primary_doc = primary_docs[i] if i < len(primary_docs) else 'Document'
                                filing_date = dates[i] if i < len(dates) else 'Unknown'
                                
                                # Build direct archive URL with CIK as integer for path
                                cik_int = int(self.cik)
                                archive_url = f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{accession}/"
                                
                                filing_urls.append({
                                    'url': archive_url,
                                    'cik': cik_int,
                                    'accession': accession,
                                    'primary_doc': primary_doc,
                                    'date': filing_date,
                                    'form': form_type
                                })
                            except (ValueError, IndexError) as e:
                                print(f"   [WARNING]  Error processing filing {i}: {e}")
                                continue
                    
                    if filing_urls:
                        print(f"[OK] Found {len(filing_urls)} {form_type} filings")
                    else:
                        print(f"   [WARNING]  No {form_type} filings found")
                    return filing_urls
                    
                except ValueError as e:
                    print(f"   [ERROR] JSON parsing error: {e}")
                    return []
            else:
                # Silently handle status codes like 404 for placeholder CIKs
                if response.status_code != 200:
                   print(f"   [INFO] No SEC filings found for this CIK (status {response.status_code})")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"   [ERROR] Network error: {e}")
            return []
        except Exception as e:
            print(f"   [ERROR] Exception in get_filing_urls: {e}")
            return []
    
    def extract_esg_text(self, filing_url):
        """
        Extract ESG-relevant text from SEC filing with improved parsing
        """
        print(f"[PARSE] Parsing filing from {filing_url['date']}")
        
        try:
            # Try multiple URL formats to find the document
            urls_to_try = []
            
            # Strategy 1: Primary document with direct filename
            if filing_url['primary_doc']:
                urls_to_try.append(f"{filing_url['url']}{filing_url['primary_doc']}")
            
            # Strategy 2: Try to find the main document by common names
            base_url = filing_url['url']
            urls_to_try.extend([
                f"{base_url}0001193125-{filing_url['accession'][6:]}-index.htm",
                f"{base_url}0001193125-{filing_url['accession'][6:]}-index.html",
                f"{base_url}{filing_url['accession']}.htm",
                f"{base_url}{filing_url['accession']}.html",
            ])
            
            # Strategy 3: Text format as last resort
            txt_url = f"https://www.sec.gov/Archives/edgar/data/{filing_url['cik']}/{filing_url['accession']}.txt"
            urls_to_try.append(txt_url)
            
            # Strategy 4: Try browsing the directory
            urls_to_try.append(base_url)
            
            response = None
            successful_url = None
            
            # Try each URL until one works
            for attempt_url in urls_to_try:
                try:
                    print(f"   [*] Trying: {attempt_url.split('/')[-1]}", end=" ")
                    response = requests.get(attempt_url, headers=self.headers, timeout=15)
                    time.sleep(0.1)
                    
                    if response.status_code == 200:
                        successful_url = attempt_url
                        print("[OK]")
                        break
                    else:
                        print(f"({response.status_code})")
                except Exception as e:
                    print(f"(error)")
                    continue
            
            if response is None or response.status_code != 200:
                print(f"   [ERROR] Could not retrieve filing from any URL format")
                return []
            
            # Parse the content
            text = response.text
            
            # If it's HTML, use BeautifulSoup
            if '<html' in text.lower() or '<body' in text.lower() or '<div' in text.lower():
                soup = BeautifulSoup(text, 'html.parser')
                # Remove script and style elements
                for script in soup(["script", "style", "table", "header", "footer"]):
                    script.decompose()
                text = soup.get_text(separator=' ', strip=True)
            
            # Clean up the text
            text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
            text = text[:100000]  # Limit to first 100K characters to avoid memory issues
            
            # ESG-specific keywords (expanded to cover all sectors)
            esg_keywords = [
                # Environmental
                'climate', 'sustainability', 'carbon', 'renewable', 'emissions', 'greenhouse',
                'environmental', 'clean energy', 'solar', 'wind', 'decarbonization', 'net zero',
                'green', 'biodiversity', 'circular', 'recycling', 'water', 'waste', 'pollution',
                'electric', 'climate change', 'eco-friendly', 'conservation', 'energy',
                'efficiency', 'reduction', 'neutral', 'impact', 'oil', 'gas', 'fuel',
                # Social & Governance
                'social', 'responsibility', 'community', 'diversity', 'equity', 'inclusion',
                'employee', 'health', 'safety', 'human', 'labor', 'wages', 'workplace',
                'discrimination', 'rights', 'supply', 'ethical', 'fair trade', 'governance',
                'disclosure', 'transparency', 'accountability', 'board', 'compensation',
                'compliance', 'ethics', 'conduct', 'anti-corruption', 'regulation', 'risk',
                # ESG and business terms
                'ESG', 'invest', 'sustainable', 'develop', 'manage', 'report', 'assess',
                'standard', 'certification', 'audit', 'practice', 'policy', 'program',
                'initiative', 'commitment', 'goal', 'target', 'measure', 'performance'
            ]
            
            # Extract sentences containing ESG keywords
            sentences = re.split(r'[.!?]+', text)
            esg_sentences = []
            
            for sentence in sentences:
                sentence = sentence.strip()
                if 30 < len(sentence) < 1000:  # Filter noise
                    sentence_lower = sentence.lower()
                    if any(keyword in sentence_lower for keyword in esg_keywords):
                        # Filter out obvious metadata/boilerplate and short fragments
                        clean_sentence = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', sentence_lower)
                        if len(clean_sentence.split()) < 5:
                            continue
                            
                        # Keywords check with higher threshold or multiple keywords
                        if any(keyword in sentence_lower for keyword in esg_keywords):
                            # Skip common boilerplate
                            if not any(x in sentence_lower for x in ['page ', 'item ', 'http', 'sec.gov', 'edgar', 'cik', 'form 10', 'table of contents', 'index', 'financial statement']):
                                esg_sentences.append(sentence)
            
            # Deduplicate similar sentences
            unique_sentences = []
            for sent in esg_sentences:
                if not any(self._similarity(sent, existing) > 0.85 for existing in unique_sentences):
                    unique_sentences.append(sent)
            
            if len(unique_sentences) > 10:
                print(f"   [OK] Extracted {len(unique_sentences)} ESG sentences")
            elif len(unique_sentences) > 0:
                print(f"   [WARNING]  Extracted {len(unique_sentences)} ESG sentences (limited)")
            else:
                print(f"   [WARNING]  No ESG content found in filing")
            
            return unique_sentences[:50]  # Return top 50 most relevant
            
        except requests.exceptions.Timeout:
            print(f"   [ERROR] Request timeout - filing too large")
            return []
        except requests.exceptions.RequestException as e:
            print(f"   [ERROR] Network error: {type(e).__name__}")
            return []
        except Exception as e:
            print(f"   [ERROR] Error: {type(e).__name__}: {str(e)[:50]}")
            return []
    
    @staticmethod
    def _similarity(s1, s2):
        """Simple Jaccard similarity for deduplication"""
        set1 = set(s1.lower().split())
        set2 = set(s2.lower().split())
        return len(set1 & set2) / len(set1 | set2) if (set1 | set2) else 0

class EnhancedSECCollector:
    """
    Expanded SEC filing collection beyond standard 10-K
    Collects comprehensive ESG-related disclosures
    """
    
    def __init__(self, ticker, cik):
        self.ticker = ticker
        self.cik = cik
        self.collector = SECDataCollector(cik, ticker)
        
    def get_comprehensive_filings(self):
        """
        Collect ESG-relevant filings beyond 10-K
        """
        print(f"[SEC] Collecting comprehensive filings for {self.ticker}")
        
        forms = ['10-K', '10-Q', 'DEF 14A', '8-K']
        all_texts = {}
        
        for form in forms:
            print(f"   [*] Searching for {form} filings...")
            urls = self.collector.get_filing_urls(form_type=form, count=2)
            
            for url_info in urls:
                texts = self.collector.extract_esg_text(url_info)
                if texts:
                    if form not in all_texts:
                        all_texts[form] = []
                    all_texts[form].extend(texts)
                    
        return all_texts
    
    def analyze_temporal_consistency(self, all_texts):
        """
        Compare sentiment across different document types
        High variance = inconsistent messaging = red flag
        """
        # Placeholder for complex analysis logic
        # In a real scenario, this would compute sentiment per form and compare
        pass
