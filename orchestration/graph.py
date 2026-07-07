from langgraph.graph import StateGraph, START, END
from orchestration.state import TradingState
from agents.analysts import fundamental_analyst, technical_analyst, sentiment_analyst, macro_analyst
from agents.researchers import bullish_researcher, bearish_researcher, research_facilitator
from agents.risk_management import conservative_risk_analyst, aggressive_risk_analyst, risk_facilitator
from agents.execution import portfolio_manager, trading_agent

def create_trading_graph() -> StateGraph:
    """Builds the Multi-Agent LangGraph workflow."""
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
    
    # Start goes to all 4 analysts (parallel execution)
    builder.add_edge(START, "fundamental")
    builder.add_edge(START, "technical")
    builder.add_edge(START, "sentiment")
    builder.add_edge(START, "macro")
    
    # All analysts must finish before researchers start
    # We do this by routing them all to the researchers
    analyst_nodes = ["fundamental", "technical", "sentiment", "macro"]
    for analyst in analyst_nodes:
        builder.add_edge(analyst, "bullish_researcher")
        builder.add_edge(analyst, "bearish_researcher")
        
    # Both researchers must finish before the facilitator summarizes
    builder.add_edge("bullish_researcher", "research_facilitator")
    builder.add_edge("bearish_researcher", "research_facilitator")
    
    # Research facilitator output goes to both risk analysts
    builder.add_edge("research_facilitator", "conservative_risk")
    builder.add_edge("research_facilitator", "aggressive_risk")
    
    # Both risk analysts must finish before the risk facilitator summarizes
    builder.add_edge("conservative_risk", "risk_facilitator")
    builder.add_edge("aggressive_risk", "risk_facilitator")
    
    # Final sequential execution
    builder.add_edge("risk_facilitator", "portfolio_manager")
    builder.add_edge("portfolio_manager", "trading_agent")
    
    # End
    builder.add_edge("trading_agent", END)
    
    return builder.compile()

