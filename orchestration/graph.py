from langgraph.graph import StateGraph, START, END
from orchestration.state import TradingState
from agents.analysts import fundamental_analyst, technical_analyst, sentiment_analyst, macro_analyst
from agents.researchers import bullish_researcher, bearish_researcher, research_facilitator
from agents.risk_management import conservative_risk_analyst, aggressive_risk_analyst, risk_facilitator
from agents.execution import portfolio_manager, trading_agent

def create_trading_graph() -> StateGraph:
    """Builds the 12-Agent LangGraph workflow (Our Main Architecture)."""
    builder = StateGraph(TradingState)
    
    # 1. Add all nodes (agents)
    builder.add_node("fundamental", fundamental_analyst)
    builder.add_node("technical", technical_analyst)
    builder.add_node("sentiment", sentiment_analyst)
    builder.add_node("macro", macro_analyst)
    
    builder.add_node("bullish_researcher", bullish_researcher)
    builder.add_node("bearish_researcher", bearish_researcher)
    builder.add_node("research_facilitator", research_facilitator)
    
    builder.add_node("conservative_risk", conservative_risk_analyst)
    builder.add_node("aggressive_risk", aggressive_risk_analyst)
    builder.add_node("risk_facilitator", risk_facilitator)
    
    builder.add_node("portfolio_manager", portfolio_manager)
    builder.add_node("trading_agent", trading_agent)
    
    # 2. Add edges
    builder.add_edge(START, "fundamental")
    builder.add_edge(START, "technical")
    builder.add_edge(START, "sentiment")
    builder.add_edge(START, "macro")
    
    analyst_nodes = ["fundamental", "technical", "sentiment", "macro"]
    for analyst in analyst_nodes:
        builder.add_edge(analyst, "bullish_researcher")
        builder.add_edge(analyst, "bearish_researcher")
        
    builder.add_edge("bullish_researcher", "research_facilitator")
    builder.add_edge("bearish_researcher", "research_facilitator")
    
    builder.add_edge("research_facilitator", "conservative_risk")
    builder.add_edge("research_facilitator", "aggressive_risk")
    
    builder.add_edge("conservative_risk", "risk_facilitator")
    builder.add_edge("aggressive_risk", "risk_facilitator")
    
    builder.add_edge("risk_facilitator", "portfolio_manager")
    builder.add_edge("portfolio_manager", "trading_agent")
    
    builder.add_edge("trading_agent", END)
    
    return builder.compile()

def create_trading_graph_8_agents() -> StateGraph:
    """Builds the 8-Agent Architecture (Ablation Study / TradingAgents Paper Clone).
    Removed: Macro Analyst, 2 Risk layers (merged to 1), Portfolio Manager (merged to Trader).
    Total: 3 Analysts + 3 Researchers + 1 Risk + 1 Trader = 8 Agents.
    """
    builder = StateGraph(TradingState)
    
    # Nodes
    builder.add_node("fundamental", fundamental_analyst)
    builder.add_node("technical", technical_analyst)
    builder.add_node("sentiment", sentiment_analyst)
    
    builder.add_node("bullish_researcher", bullish_researcher)
    builder.add_node("bearish_researcher", bearish_researcher)
    builder.add_node("research_facilitator", research_facilitator)
    
    # Use conservative risk as the single risk manager
    builder.add_node("risk_manager", conservative_risk_analyst) 
    builder.add_node("trading_agent", trading_agent)
    
    # Edges
    builder.add_edge(START, "fundamental")
    builder.add_edge(START, "technical")
    builder.add_edge(START, "sentiment")
    
    analyst_nodes = ["fundamental", "technical", "sentiment"]
    for analyst in analyst_nodes:
        builder.add_edge(analyst, "bullish_researcher")
        builder.add_edge(analyst, "bearish_researcher")
        
    builder.add_edge("bullish_researcher", "research_facilitator")
    builder.add_edge("bearish_researcher", "research_facilitator")
    
    builder.add_edge("research_facilitator", "risk_manager")
    builder.add_edge("risk_manager", "trading_agent")
    
    builder.add_edge("trading_agent", END)
    
    return builder.compile()

def create_trading_graph_1_agent() -> StateGraph:
    """Builds the 1-Agent Architecture (Ablation Study).
    A single LLM gets all raw data and makes the trading decision alone.
    """
    builder = StateGraph(TradingState)
    
    # Node: Just the trading agent doing everything
    builder.add_node("trading_agent", trading_agent)
    
    # Edges
    builder.add_edge(START, "trading_agent")
    builder.add_edge("trading_agent", END)
    
    return builder.compile()

