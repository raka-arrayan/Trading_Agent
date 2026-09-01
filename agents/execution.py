from orchestration.state import TradingState
from config.llm_config import get_llm
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
import config.prompts.execution_prompts as prompts
import json
import re


def _extract_strategy(text: str) -> str:
    """Extract dominant strategy keyword (BUY/SELL/HOLD) from LLM response text."""
    if not text:
        return "HOLD"
    upper = str(text).upper()
    buy_count = len(re.findall(r'\bBUY\b', upper))
    sell_count = len(re.findall(r'\bSELL\b', upper))
    hold_count = len(re.findall(r'\bHOLD\b', upper))
    
    counts = {"BUY": buy_count, "SELL": sell_count, "HOLD": hold_count}
    return max(counts, key=counts.get) if max(counts.values()) > 0 else "HOLD"


def _clean_text(text: str) -> str:
    """Clean text for log display without truncating."""
    if not text:
        return "(kosong)"
    return text.replace('\n', ' ').strip()


def portfolio_manager(state: TradingState):
    print("--- Running Portfolio Manager ---")
    llm = get_llm("analyst", "gemini")
    
    res_cons = state.get("research_consensus", "")
    risk_cons = state.get("risk_consensus", "")
    portfolio = state.get("portfolio_status", {})
    
    sys_msg = SystemMessage(content=prompts.PORTFOLIO_MANAGER_PROMPT)
    human_msg = HumanMessage(content=f"Research Consensus:\n{res_cons}\n\nRisk Consensus:\n{risk_cons}\n\nPortfolio Status:\n{json.dumps(portfolio, indent=2)}")
    
    try:
        response = llm.invoke([sys_msg, human_msg])
        decision = response.content
    except Exception as e:
        print(f"[PM] LLM Error: {e}")
        decision = f"Error generating decision: {e}"

    # Print moved to backtester.py
        
    new_portfolio = portfolio.copy() if portfolio else {}
    new_portfolio["recommendation"] = decision
    return {"portfolio_status": new_portfolio}

def trading_agent(state: TradingState):
    print("--- Running Trading Agent ---")
    llm = get_llm("analyst", "gemini")
    
    pm_rec = state.get("portfolio_status", {}).get("recommendation", "")
    
    sys_msg = SystemMessage(content=prompts.TRADING_AGENT_PROMPT)
    human_msg = HumanMessage(content=f"Portfolio Manager Recommendation:\n{pm_rec}")
    
    try:
        response = llm.invoke([sys_msg, human_msg])
        content = response.content
        if isinstance(content, list):
            content = " ".join([c.get("text", "") if isinstance(c, dict) else str(c) for c in content])
        
        
        # Use regex to find JSON block if LLM added markdown formatting
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            decision = json.loads(json_match.group(0))
        else:
            # Fallback to direct parsing
            parser = JsonOutputParser()
            decision = parser.parse(content)
            
    except Exception as e:
        print(f"[Trader] LLM/Parse Error: {e}")
        decision = {"action": "HOLD", "quantity": 0, "confidence": 0.0, "raw_error": str(e)}

    return {"trading_decision": decision}
