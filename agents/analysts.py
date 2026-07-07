from orchestration.state import TradingState
from config.llm_config import get_llm
from langchain_core.messages import HumanMessage, SystemMessage
import config.prompts.analyst_prompts as prompts
import json

def _run_analyst_node(state: TradingState, role_name: str, data_key: str, prompt_template: str) -> dict:
    """Helper to run a generic analyst node."""
    print(f"--- Running {role_name} Analyst ---")
    llm = get_llm("analyst", "ollama")
    
    sys_msg = SystemMessage(content=prompt_template)
    
    # Extract the relevant data from the state
    market_data = state.get("market_data", {})
    data_content = market_data.get(data_key, {})
    
    # Format data as JSON string for the LLM
    data_str = json.dumps(data_content, indent=2)
    
    # Ensure it's not too long for the context window (Ollama 8b has ~8k context, but we keep it reasonable)
    if len(data_str) > 3000:
        data_str = data_str[:3000] + "\n...[TRUNCATED]"
        
    human_msg = HumanMessage(content=f"Ticker: {state.get('ticker')}\nDate: {state.get('date')}\n\nData:\n{data_str}")
    
    try:
        response = llm.invoke([sys_msg, human_msg])
        report = response.content
    except Exception as e:
        print(f"[{role_name}] LLM Error: {e}")
        report = f"Error generating report: {e}"
        
    return {"analyst_reports": {role_name.lower(): report}}


def fundamental_analyst(state: TradingState):
    return _run_analyst_node(state, "Fundamental", "fundamentals", prompts.FUNDAMENTAL_ANALYST_PROMPT)

def technical_analyst(state: TradingState):
    return _run_analyst_node(state, "Technical", "indicators", prompts.TECHNICAL_ANALYST_PROMPT)

def sentiment_analyst(state: TradingState):
    return _run_analyst_node(state, "Sentiment", "news", prompts.SENTIMENT_ANALYST_PROMPT)

def macro_analyst(state: TradingState):
    return _run_analyst_node(state, "Macro", "news", prompts.MACRO_ANALYST_PROMPT)

