from orchestration.state import TradingState
from config.llm_config import get_llm
from langchain_core.messages import HumanMessage, SystemMessage
import config.prompts.risk_prompts as prompts
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


def conservative_risk_analyst(state: TradingState):
    print("--- Running Conservative Risk Analyst ---")
    llm = get_llm("researcher", "gemini")
    
    consensus = state.get("research_consensus", "")
    
    sys_msg = SystemMessage(content=prompts.CONSERVATIVE_RISK_PROMPT)
    human_msg = HumanMessage(content=f"Research Consensus:\n{consensus}")
    
    try:
        response = llm.invoke([sys_msg, human_msg])
        argument = response.content
    except Exception as e:
        print(f"[Cons_Risk] LLM Error: {e}")
        argument = f"Error generating argument: {e}"

    # Print moved to backtester.py
        
    return {"risk_debate": [{"agent": "ConservativeRisk", "message": argument}]}

def aggressive_risk_analyst(state: TradingState):
    print("--- Running Aggressive Risk Analyst ---")
    llm = get_llm("researcher", "gemini")
    
    consensus = state.get("research_consensus", "")
    
    sys_msg = SystemMessage(content=prompts.AGGRESSIVE_RISK_PROMPT)
    human_msg = HumanMessage(content=f"Research Consensus:\n{consensus}")
    
    try:
        response = llm.invoke([sys_msg, human_msg])
        argument = response.content
    except Exception as e:
        print(f"[Aggr_Risk] LLM Error: {e}")
        argument = f"Error generating argument: {e}"

    # Print moved to backtester.py
        
    return {"risk_debate": [{"agent": "AggressiveRisk", "message": argument}]}

def risk_facilitator(state: TradingState):
    print("--- Running Risk Facilitator ---")
    llm = get_llm("analyst", "gemini")
    
    debate = state.get("risk_debate", [])
    consensus = state.get("research_consensus", "")
    
    sys_msg = SystemMessage(content=prompts.RISK_FACILITATOR_PROMPT)
    human_msg = HumanMessage(content=f"Original Research Consensus:\n{consensus}\n\nRisk Debate:\n{json.dumps(debate, indent=2)}")
    
    try:
        response = llm.invoke([sys_msg, human_msg])
        final_consensus = response.content
    except Exception as e:
        print(f"[Risk_Facilitator] LLM Error: {e}")
        final_consensus = f"Error generating consensus: {e}"

    # Print moved to backtester.py
        
    return {"risk_consensus": final_consensus}
