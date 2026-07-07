from orchestration.state import TradingState
from config.llm_config import get_llm
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
import config.prompts.execution_prompts as prompts
import json
import re

def portfolio_manager(state: TradingState):
    print("--- Running Portfolio Manager ---")
    llm = get_llm("analyst", "ollama")
    
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
        
    new_portfolio = portfolio.copy() if portfolio else {}
    new_portfolio["recommendation"] = decision
    return {"portfolio_status": new_portfolio}

def trading_agent(state: TradingState):
    print("--- Running Trading Agent ---")
    llm = get_llm("analyst", "ollama")
    
    pm_rec = state.get("portfolio_status", {}).get("recommendation", "")
    
    sys_msg = SystemMessage(content=prompts.TRADING_AGENT_PROMPT)
    human_msg = HumanMessage(content=f"Portfolio Manager Recommendation:\n{pm_rec}")
    
    try:
        response = llm.invoke([sys_msg, human_msg])
        content = response.content
        
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
