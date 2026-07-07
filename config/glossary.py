INDONESIAN_FINANCIAL_GLOSSARY = """
# Indonesian Financial Terms Glossary
Use this glossary to translate and understand Indonesian financial and banking terms found in the data/news:
- IHSG (Indeks Harga Saham Gabungan) = Jakarta Composite Index (JCI). The main index of the Indonesia Stock Exchange.
- Emiten = Listed company / Issuer.
- DPK (Dana Pihak Ketiga) = Third-Party Funds (Customer deposits like savings, checking, and time deposits).
- NPL (Non-Performing Loan) = A metric for credit risk. Lower is better. NPL Gross < 5% is the regulatory threshold in Indonesia.
- NIM (Net Interest Margin) = Profitability from interest-earning assets. Indonesian banks typically have high NIMs (4% - 6%).
- CAR (Capital Adequacy Ratio) = Capital buffer to absorb losses. Regulatory minimum is usually 8%, but big banks maintain >18%.
- Laba Bersih = Net Profit / Net Income.
- Suku Bunga Acuan (BI-Rate / BI-7DRR) = The benchmark interest rate set by Bank Indonesia (the central bank).
- OJK (Otoritas Jasa Keuangan) = Financial Services Authority. The regulator of the financial sector.
- Kredit Macet = Bad debt / Defaulted loans.
- LDR (Loan to Deposit Ratio) = Liquidity metric.
- Saham = Stock / Share.
- Perbankan = Banking sector.
"""

def get_glossary_prompt() -> str:
    """Returns the glossary to be injected into system prompts."""
    return INDONESIAN_FINANCIAL_GLOSSARY
