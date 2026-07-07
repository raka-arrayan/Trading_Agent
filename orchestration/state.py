from typing import TypedDict, Dict, Any, List, Annotated
import operator

def update_dict(dict1: dict, dict2: dict) -> dict:
    """Reducer to merge dictionaries in the state."""
    if dict1 is None:
        dict1 = {}
    if dict2 is None:
        dict2 = {}
    return {**dict1, **dict2}

def append_list(list1: list, list2: list) -> list:
    """Reducer to append items to a list in the state."""
    if list1 is None:
        list1 = []
    if list2 is None:
        list2 = []
    # If list2 is a single item that isn't a list, wrap it
    if not isinstance(list2, list):
        list2 = [list2]
    return list1 + list2

class TradingState(TypedDict):
    """
    Global state schema for the Multi-Agent Trading System.
    Uses Annotated with custom reducers for dictionary/list updates so parallel agents
    can update different keys in the same dictionary without overwriting each other.
    """
    # Base inputs
    ticker: str
    date: str
    
    # 1. Market Data
    market_data: Dict[str, Any]
    
    # 2. Analyst Reports (Parallel execution)
    # e.g. {"fundamental": "...", "technical": "...", "sentiment": "...", "macro": "..."}
    analyst_reports: Annotated[Dict[str, str], update_dict]
    
    # 3. Research Debate
    # Messages from Bullish and Bearish researchers
    research_debate: Annotated[List[Dict[str, str]], append_list]
    research_consensus: str
    
    # 4. Risk Assessment
    # e.g. {"market_risk": "...", "credit_risk": "...", "liquidity_risk": "..."}
    risk_reports: Annotated[Dict[str, str], update_dict]
    risk_debate: Annotated[List[Dict[str, str]], append_list]
    risk_consensus: str
    
    # 5. Portfolio Context
    portfolio_status: Dict[str, Any]
    
    # 6. Final Output
    trading_decision: Dict[str, Any]
