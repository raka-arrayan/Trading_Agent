import sys
from pathlib import Path
import json

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from orchestration.graph import create_trading_graph

def run_graph_smoke_test():
    print("Initializing Multi-Agent LangGraph...")
    app = create_trading_graph()
    
    # Initialize a dummy state for BBCA
    initial_state = {
        "ticker": "BBCA.JK",
        "date": "2024-01-31",
        "market_data": {
            "fundamentals": {"P/E": 13.2},
            "indicators": {"MACD": 65.2, "RSI": 53.6},
            "news": [{"title": "IHSG Hijau, Saham BBCA Naik", "source": "CNBC"}]
        },
        "analyst_reports": {},
        "research_debate": [],
        "research_consensus": "",
        "risk_reports": {},
        "risk_debate": [],
        "risk_consensus": "",
        "portfolio_status": {"current_cash": 100000000, "positions": {}},
        "trading_decision": {}
    }
    
    print("\nStarting execution of 13-Agent Graph...")
    print("Note: If Ollama is not running on localhost:11434, agents will gracefully fallback to DUMMY text.")
    print("="*50)
    
    # Execute the graph
    try:
        final_state = app.invoke(initial_state)
        
        print("\n" + "="*50)
        print("GRAPH EXECUTION COMPLETED")
        print("="*50)
        
        print("\n[Analyst Reports]")
        for role, report in final_state.get('analyst_reports', {}).items():
            print(f"- {role.capitalize()}: {report}")
            
        print("\n[Research Debate]")
        for message in final_state.get('research_debate', []):
            print(f"- {message['agent']}: {message['message']}")
            
        print("\n[Research Consensus]")
        print(final_state.get('research_consensus'))
            
        print("\n[Risk Debate]")
        for message in final_state.get('risk_debate', []):
            print(f"- {message['agent']}: {message['message']}")
            
        print("\n[Risk Consensus]")
        print(final_state.get('risk_consensus'))
            
        print("\n[Portfolio Recommendation]")
        print(final_state.get('portfolio_status', {}).get('recommendation'))
        
        print("\n[FINAL TRADING DECISION]")
        print(json.dumps(final_state.get('trading_decision'), indent=2))
        
    except Exception as e:
        print(f"\nGraph Execution Failed: {e}")

if __name__ == "__main__":
    run_graph_smoke_test()
