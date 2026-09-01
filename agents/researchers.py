from orchestration.state import TradingState
from config.llm_config import get_llm
from langchain_core.messages import HumanMessage, SystemMessage
import config.prompts.research_prompts as prompts
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


def bullish_researcher(state: TradingState):
    print("--- Running Bullish Researcher ---")
    llm = get_llm("researcher", "gemini")
    
    reports = state.get("analyst_reports", {})
    
    sys_msg = SystemMessage(content=prompts.BULLISH_PROMPT)
    human_msg = HumanMessage(content=f"Analyst Reports:\n{json.dumps(reports, indent=2)}")
    
    try:
        response = llm.invoke([sys_msg, human_msg])
        argument = response.content
    except Exception as e:
        print(f"[Bullish] LLM Error: {e}")
        argument = f"Error generating argument: {e}"

    # Print moved to backtester.py for sequential ordering
        
    return {"research_debate": [{"agent": "Bullish", "message": argument}]}

def bearish_researcher(state: TradingState):
    print("--- Running Bearish Researcher ---")
    llm = get_llm("researcher", "gemini")
    
    reports = state.get("analyst_reports", {})
    
    sys_msg = SystemMessage(content=prompts.BEARISH_PROMPT)
    human_msg = HumanMessage(content=f"Analyst Reports:\n{json.dumps(reports, indent=2)}")
    
    try:
        response = llm.invoke([sys_msg, human_msg])
        argument = response.content
    except Exception as e:
        print(f"[Bearish] LLM Error: {e}")
        argument = f"Error generating argument: {e}"

    # Print moved to backtester.py
        
    return {"research_debate": [{"agent": "Bearish", "message": argument}]}

def research_facilitator(state: TradingState):
    print("--- Running Research Facilitator ---")
    llm = get_llm("analyst", "gemini")
    
    debate = state.get("research_debate", [])
    
    sys_msg = SystemMessage(content=prompts.RESEARCH_FACILITATOR_PROMPT)
    human_msg = HumanMessage(content=f"Debate Arguments:\n{json.dumps(debate, indent=2)}")
    
    try:
        response = llm.invoke([sys_msg, human_msg])
        consensus = response.content
    except Exception as e:
        print(f"[Facilitator] LLM Error: {e}")
        consensus = f"Error generating consensus: {e}"

    # Print moved to backtester.py
        
    return {"research_consensus": consensus}
