import sys
import json
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from orchestration.state import TradingState
from agents.analysts import fundamental_analyst

def test_single_agent():
    print("Testing Fundamental Analyst with Real Prompt and Dummy Data...")
    
    # Mock pipeline data
    initial_state = {
        "ticker": "BBCA.JK",
        "date": "2024-01-31",
        "market_data": {
            "fundamentals": {
                "company_name": "Bank Central Asia Tbk",
                "sector": "Banking",
                "pe_ratio": 15.2,
                "pbv": 4.1,
                "roe": 22.5,
                "npl_gross": 1.2,
                "car": 25.4,
                "nim": 5.8
            }
        },
        "analyst_reports": {},
        "research_debate": [],
        "research_consensus": "",
        "risk_reports": {},
        "risk_debate": [],
        "risk_consensus": "",
        "portfolio_status": {},
        "trading_decision": {}
    }
    
    # Run just the fundamental node
    result = fundamental_analyst(initial_state)
    
    print("\n[Result from Fundamental Analyst]")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_single_agent()
